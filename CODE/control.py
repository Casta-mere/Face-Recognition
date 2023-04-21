from database import database
# from mail import mail
from face import addface
from IP import IP
from Log import log

import time
import datetime
import asyncio
import base64
import threading
import websockets
import face_recognition
import numpy as np
import os
import cv2
import sys
import ssl

time_sep = 300              # 间隔时间
IP_ADDR = IP.get_ip()       # 服务器IP地址
IP_PORT = "8888"            # 服务器端口号
sourcedir = 'face/faceImg/source.jpg'


class control():

    def __init__(self):
        self.init_log()
        self.init_db()

        # self.mail=mail()
        self.info = {}
        self.user_status = {}

        self.load_info()
        self.renew_status()
        self.recognition = control.recognize(self.info, self)
        self.recognition.start()
        self.msg = ""

        success = "SUCCESS : Server is running on https://{}:{}".format(
            IP_ADDR, "8500")
        print(success)
        self.log.log(success)

    def init_log(self):
        os.system('cls')
        self.log = log.log()
        self.log.log("====================================================================")
        self.log.log("NEW INSTANCE RUNNING")

    def init_db(self):
        self.database = database.my_sql('facerecognition')
        state, msg = self.database.boot_selftest()
        self.log.log(msg)
        print(msg)
        if not state:
            sys.exit(0)

    def get_msg(self):
        time.sleep(0.5)
        yield self.msg

    def get_id(self, username):
        dict = {v[0]: k for k, v in self.info.items()}
        return dict[username]

    def load_info(self):
        self.info = {}
        l = list(self.database.get_all_data('info'))
        for i in l:
            self.info[i[0]] = [i[1], i[2]]

    def now_time(self):
        nowdate = time.strftime('%Y-%m-%d', time.localtime())
        nowtime = time.strftime('%H:%M:%S', time.localtime())
        return nowdate, nowtime

    def renew_status(self):
        self.user_status = {}
        for i in list(self.info.keys()):
            l = list(self.database.get_newest_data('entry', i))[0]
            status = bool(l[-1])
            if(status):
                nowtime = datetime.datetime.strptime(str(l[3]), '%H:%M:%S')
            else:
                nowtime = datetime.datetime.strptime(str(l[4]), '%H:%M:%S')
            self.user_status[i] = [status, nowtime]

    def getin(self, userid):
        d, t = self.now_time()
        entry = [userid, self.info[userid][0], d, t, '', True]
        self.database.add_new_entry('entry', entry)
        self.renew_status()

    def getout(self, userid):
        d, t = self.now_time()
        self.database.update_table_entry(userid, t)
        self.renew_status()

    def initial_user(self, userid):
        d, t = time.strftime('%Y-%m-%d', time.localtime()), '00:00:00'
        entry = [userid, self.info[userid][0], d, t, t, False]
        self.database.add_new_entry('entry', entry)
        self.renew_status()

    def is_valid(self, userid):
        lasttime = self.user_status[userid][1]
        # print(lasttime,type(lasttime))
        d, t = self.now_time()
        nowtime = datetime.datetime.strptime(t, '%H:%M:%S')
        dalta = nowtime-lasttime
        dalta = int(dalta.total_seconds())
        # print(dalta,type(dalta))

        if dalta*dalta > time_sep*time_sep:
            return True
        else:
            return False

    def check(self, userid):
        valid = self.is_valid(userid)
        status = self.user_status[userid][0]
        self.msg = ""

        if(not valid and status):
            self.msg = f"{self.info[userid][0]}请勿重复签到"
        elif(not valid and not status):
            self.msg = f"{self.info[userid][0]}请勿重复签退"
        elif(valid and status):
            self.getout(userid)
            self.msg = f"{self.info[userid][0]}签退成功"
            time.sleep(3)
        elif(valid and not status):
            self.getin(userid)
            self.msg = f"{self.info[userid][0]}签到成功"
            time.sleep(3)
        return self.msg

    def adduser(self, name, email):
        # userid 为空闲的最小id
        userid = 1
        while(userid in self.info.keys()):
            userid += 1

        try:
            self.recognition.stop()

            state, msg = addface.addface_frompic(userid)
            if(not state):
                self.log.log(msg)
                return False, "未检测到人脸，请站远一点再重试"

            self.log.log(msg+f", username : {name}")
            info = [userid, name, email]
            self.database.add_new_entry('info', info)
            self.load_info()
            self.initial_user(userid)
            self.renew_status()

            self.recognition.load_faces(self.info)
            self.recognition.restart()

            msg = f"SUCCESS : 新用户{name}添加成功"
            return True, msg

        except:
            msg = f"ERROR IN {sys._getframe().f_code.co_name}"
            self.log.log(msg)
            return False, msg

    def deleteuser(self, username):
        try:
            userid = self.get_id(username)
        except:
            msg = f"ERROR : user {username} not exist!"
            self.log.log(msg)
            msg = f"用户{username}不存在"
            return False, msg

        self.database.delete_table_entry('info', userid)
        self.database.delete_table_entry('entry', userid)
        addface.deleteface(userid)
        self.load_info()
        self.renew_status()
        self.recognition.load_faces(self.info)

        msg = f"SUCCESS : user {username} deleted!"
        self.log.log(msg)
        msg = f"SUCCESS : 用户{username}删除成功"
        return True, msg

    class recognize():

        def __init__(self, dictionary, obj):
            self.frame_stack = []
            self.width = 0
            self.height = 0
            self.target_size = (1500, 1500)
            self.img_path = 'face/faceImg'
            self.npy_path = 'face/faceNpy'
            self.known_face_encodings = []
            self.known_face_names = []
            self.load_faces(dictionary)
            self.obj = obj
            self.flagDetect = False
            self.falgRestart = False
            self.flagLoad = False
            self.server = control.recognize.Server(self)
            self.server.start_server()

        def load_faces(self, dictionary):
            t=time.time()
            self.flagLoad = True
            self.known_face_encodings = []
            self.known_face_names = []
            for i in dictionary.keys():
                npy_path = f'{self.npy_path}/{i}.npy'
                try:
                    face_encoding = np.load(npy_path)
                    self.known_face_encodings.append(face_encoding)
                    self.known_face_names.append(dictionary[i][0])
                except:
                    print(f"ERROR : {dictionary[i]} not exist")
            self.flagLoad = False
            print("load faces cost : "+str(time.time()-t))
            print(f"total {len(self.known_face_encodings)} faces loaded")

        def response(self, state, name="", confidence=0):
            if state == True:
                # print(name + " " + str(confidence))
                return(name + " " + str(confidence))
            else:
                # print("ERROR : no face recognized")
                self.obj.msg = ""
                return("ERROR : no face recognized")

        def detect_faces(self):
            while True:
                if self.falgRestart:
                    continue
                if not self.flagDetect:
                    continue
                if self.flagLoad:
                    continue
                if len(self.frame_stack) == 0:
                    continue
                frame = self.frame_stack.pop()
                self.frame_stack = []

                # frame=cv2.resize(frame,self.target_size)
                # cv2.imwrite(sourcedir,frame)

                face_locations = face_recognition.face_locations(frame)
                face_encodings = face_recognition.face_encodings(
                    frame, face_locations)
                if len(face_locations) == 0:
                    self.response(False)
                else:
                    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                        matches = face_recognition.compare_faces(
                            self.known_face_encodings, face_encoding)
                        name = "Unknown"
                        face_distances = face_recognition.face_distance(
                            self.known_face_encodings, face_encoding)
                        best_match_index = np.argmin(face_distances)
                        confidence = 1 - face_distances[best_match_index]
                        if matches[best_match_index] and confidence > 0.6:
                            name = self.known_face_names[best_match_index]
                            self.response(True, name, confidence)
                            self.obj.check(self.obj.get_id(name))
                            # print(self.obj.check(self.obj.get_id(name)))
                        else:
                            self.response(True, "unknown", confidence)

        def start(self):
            t = threading.Thread(target=self.detect_faces)
            t.start()

        def stop(self):
            self.flagRestart = True
            print("ALERT : Detect stopped!")

        def restart(self):
            self.flagRestart = False
            print("SUCCESS : Detect restarted!")

        class Server():

            def __init__(self, obj):
                self.IP_ADDR = IP_ADDR
                self.IP_PORT = IP_PORT
                self.obj = obj

            def start_server(self):
                t = threading.Thread(target=self.start)
                t.start()

            def start(self):
                msg = "ALERT : Waiting for Connection"
                self.obj.obj.log.log(msg)
                print(msg)

                asyncio.set_event_loop(asyncio.new_event_loop())
                ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
                ssl_context.load_cert_chain(
                    certfile="static/servercert/server-cert.pem", keyfile="static/servercert/server-key.pem")
                self.server = websockets.serve(
                    self.serverRun, self.IP_ADDR, self.IP_PORT, ssl=ssl_context)
                asyncio.get_event_loop().run_until_complete(self.server)
                asyncio.get_event_loop().run_forever()

            async def serverHands(self, websocket):
                while True:
                    recv_text = await websocket.recv()
                    if recv_text == "hello":
                        await websocket.send("123")
                        return True
                    else:
                        await websocket.send("connected fail")

            # receive the video from client and show it in the window using opencv
            async def serverRecv(self, websocket):
                while True:
                    recv_text = await websocket.recv()
                    if "data:image/jpeg;base64," in recv_text:
                        recv_text = recv_text.replace(
                            "data:image/jpeg;base64,", "")
                        imgdata = base64.b64decode(recv_text)
                        image = cv2.imdecode(np.frombuffer(
                            imgdata, np.uint8), cv2.IMREAD_COLOR)
                        if(len(self.obj.frame_stack) > 50):
                            self.obj.fraem_stack = []
                        # print(image.shape)
                        self.obj.frame_stack.append(image)
                        # cv2.imshow("server", image)
                        # cv2.waitKey(1)

            # handshake with client
            async def serverRun(self, websocket):
                await self.serverHands(websocket)
                msg = f"SUCCESS : Connection start on {self.IP_ADDR}:{self.IP_PORT}"
                self.obj.obj.log.log(msg)
                print(msg)

                self.obj.flagDetect = True
                try:
                    await self.serverRecv(websocket)
                except websockets.exceptions.ConnectionClosed:
                    self.obj.flagDetect = False
                    msg = f"ALERT : Connection closed on {self.IP_ADDR}:{self.IP_PORT}"
                    self.obj.obj.log.log(msg)
                    print(msg)
                    msg = f"ALERT : Waiting for Reconnection on {self.IP_ADDR}:{self.IP_PORT}"
                    self.obj.obj.log.log(msg)
                    print(msg)


if __name__ == "__main__":
    os.system('cls')
    # c = control()
