from database import database
# from mail import mail
from face import addface
from IP import IP
from Log import log

import dlib
import csv
import time
import datetime
import asyncio
import base64
import threading
import websockets
import numpy as np
import pandas as pd
import os
import cv2
import sys
import ssl

time_sep = 300              # 间隔时间
IP_ADDR = IP.get_ip()       # 服务器IP地址
IP_PORT = 8100           # 服务器端口号
source_pic_dir = 'face/faceImg/source.jpg'
source_csv_dir = 'face/faceImg/features.csv'
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('face/data_dlib/shape_predictor_68_face_landmarks.dat')
face_reco_model = dlib.face_recognition_model_v1("face/data_dlib/dlib_face_recognition_resnet_model_v1.dat")


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
    
        self.clientDict={}
        self.IP_PORT=8100

        success = "SUCCESS : Server is running on https://{}:{}".format(
            IP_ADDR, "8500")
        print(success)
        self.log.log(success)
 
    def init_log(self):
        os.system('cls')
        self.log = log.log()
        
    def init_db(self):
        self.database = database.my_sql('facerecognition')
        state, msg = self.database.boot_selftest()
        self.log.log(msg)
        print(msg)
        if not state:
            sys.exit(0)

    def add_client(self):
        if(self.IP_PORT==8200):
            self.IP_PORT=8100
        if(self.IP_PORT in self.clientDict.keys()):
            self.IP_PORT+=1

        msg,client=self.recognition.add_client(self.IP_PORT,1)

        self.clientDict[self.IP_PORT]=client

        msg=f"SUCCESS : Add new Client {self.IP_PORT}"
        print(msg)
        self.log.log(msg)

        msg=f"SUCCESS : Totoal {len(self.clientDict)} clients : {list(self.clientDict.keys())}"
        print(msg)
        self.log.log(msg)
        
        return self.IP_PORT,client
        
    def set_client_type(self,PORT,Type):
        self.clientDict[PORT].Type=Type

    def del_client(self,PORT):
        self.recognition.del_client(PORT)
        del self.clientDict[PORT]

        msg=f"SUCCESS : Remove Client {PORT}"
        print(msg)
        self.log.log(msg)

        msg=f"SUCCESS : Totoal {len(self.clientDict)} clients : {list(self.clientDict.keys())}"
        print(msg)
        self.log.log(msg)

    def get_msg(self,clientid):
        msg=self.clientDict[clientid].get_msg()
        # print(msg)
        return msg

    def get_id(self, username):
        dict = {v[0]: k for k, v in self.info.items()}
        return dict[username]

    def load_info(self):
        self.info = {}
        l = list(self.database.get_all_data('info'))
        for i in l:
            self.info[eval(i[0])] = [i[1], i[2]]

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

    def check(self, userid, id):
        valid = self.is_valid(userid)
        status = self.user_status[userid][0]
        client = self.clientDict[id]
        tpye = client.get_type()
        client.msg = ""

        switch = {1: "签到签退", 2: "签到", 3: "签退"}

        if tpye == 1:
            if(not valid and status):
                client.msg = f"{self.info[userid][0]}请勿重复签到"
            elif(not valid and not status):
                client.msg = f"{self.info[userid][0]}请勿重复签退"
            elif(valid and status):
                self.getout(userid)
                client.msg = f"{self.info[userid][0]}签退成功"
                time.sleep(3)
            elif(valid and not status):
                self.getin(userid)
                client.msg = f"{self.info[userid][0]}签到成功"
                time.sleep(3)

        elif tpye == 2:
            if(not valid and status):
                client.msg = f"{self.info[userid][0]}请勿重复签到"
            elif(valid and not status):
                self.getin(userid)
                client.msg = f"{self.info[userid][0]}签到成功"
                time.sleep(3)
            else:
                client.msg = f"该设备只能进行{switch[tpye]}操作"

        elif tpye == 3:
            if(not valid and not status):
                client.msg = f"{self.info[userid][0]}请勿重复签退"
            elif(valid and status):
                self.getout(userid)
                client.msg = f"{self.info[userid][0]}签退成功"
                time.sleep(3)
            else:
                client.msg = f"该设备只能进行{switch[tpye]}操作"
        return client.msg

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
            info = [str(userid), name, email]
            self.database.add_new_entry('info', info)
            self.load_info()
            self.initial_user(userid)
            self.renew_status()

            self.recognition.update_faces_add(self.info)
            self.recognition.restart()

            msg = f"SUCCESS : 新用户{name}添加成功"
            return True, msg

        except:
            msg = f"ERROR IN {sys._getframe().f_code.co_name}"
            self.log.log(msg)
            return False, msg

    def deleteuser(self, userid_list):
        message = "SUCCESS : 删除成功"
        flag = False
        for userid in userid_list:
            username=self.info[eval(userid)][0]

            self.database.delete_table_entry('info', userid)
            self.database.delete_table_entry('entry', userid)
            state, msg = addface.deleteface(eval(userid))
            
            self.log.log(msg)

            self.load_info()
            self.renew_status()
            self.recognition.update_faces_delete(username)

            msg = f"SUCCESS : user {username} (usrid {userid}) deleted!"
            self.log.log(msg)
            print(msg)

        return True, message

    class recognize():

        def __init__(self, dictionary, obj):
            self.obj = obj
            self.features_known_list = []
            self.known_face_names = []
            self.img_path = 'face/faceImg'

            self.frame_queue = []

            self.client={}

            self.load_faces(dictionary)

            self.flagDetect = True
            self.flagRestart = False
            self.flagLoad = False # weather is loading faces
            # self.server = control.recognize.Server(self)
            # self.server.start_server()

        def load_faces(self, dictionary):
            t=time.time()
            self.flagLoad = True
            self.features_known_list = []
            self.known_face_names = []

            # print(dictionary.keys())
            with open(source_csv_dir,'r') as file:
                reader=csv.reader(file)
                for i in reader:
                    id = eval(i[0])
                    if(id not in dictionary.keys()):
                        continue
                    # print(f"id = {id}")
                    face_encoding = [float(x) for x in i[1:]]
                    self.known_face_names.append(dictionary[id][0])
                    self.features_known_list.append(face_encoding)


                    # self.obj.log.log("ERROR : "+str(e)+" in load_faces")
                    # print(f"ERROR : {dictionary[i]} not exist")
            
            self.flagLoad = False

            msg = "SUCCESS : load faces cost : "+str(time.time()-t)
            self.obj.log.log(msg)
            print(msg)

            msg = f"SUCCESS : total {len(self.known_face_names)} faces loaded"
            self.obj.log.log(msg)
            print(msg)

        def update_faces_add(self,dictionary):
            self.flagLoad = True

            csv_rd = pd.read_csv(source_csv_dir, header=None)
            id = csv_rd.iloc[-1][0]
            name = dictionary[id][0]
            feature = csv_rd.iloc[-1][1:].values.astype(float).tolist()

            self.known_face_names.append(name)
            self.features_known_list.append(feature) 

            self.flagLoad = False

        def update_faces_delete(self, username):
            self.flagLoad = True

            for i in self.known_face_names:
                if (username == i):
                    self.features_known_list.pop(self.known_face_names.index(i))
                    self.known_face_names.remove(i)
                    break
            
            self.flagLoad = False
            

        def is_image_in_queue(self,id):
            return not self.client[id][1]

        def update_image_in_queue(self,id,frame):
            self.frame_queue.insert(0,[id,frame])
            self.client[id][1]=True
        
        def image_processed(self,id):
            # print(f'processed with device {id}')
            self.client[id][1]=False
            # pass

        def add_client(self,PORT,Type):
            self.client[PORT]=[self.Client(self,IP_ADDR,PORT,Type,PORT),False]
            self.client[PORT][0].start_client()

            return "SUCCESS",self.client[PORT][0]

        def del_client(self,IP_PORT):
            del self.client[IP_PORT]

        def response(self, state, name="", confidence=0):
            if state == True:
                # print(name + " " + str(confidence))
                return(name + " " + str(confidence))
            else:
                # print("ERROR : no face recognized")
                self.obj.msg = ""
                return("ERROR : no face recognized")

        @staticmethod
        def return_euclidean_distance(feature_1, feature_2):
            feature_1 = np.array(feature_1)
            feature_2 = np.array(feature_2)
            dist = np.sqrt(np.sum(np.square(feature_1 - feature_2)))
            return dist

        def detect_faces(self):
            while True:
                if self.flagRestart:
                    continue
                if not self.flagDetect:
                    continue
                if self.flagLoad:
                    continue
                if len(self.frame_queue) == 0:
                    continue
                
                
                info = self.frame_queue.pop()
                id=info[0]
                frame=info[1]

                faces = detector(frame, 0)
                face_cnt = len (faces)

                if face_cnt != 1:
                    self.obj.clientDict[id].msg = ""
                else:
                    shape = predictor(frame, faces[0])
                    current_face_feature = face_reco_model.compute_face_descriptor(frame, shape)
                    current_face_distance = []

                    for i in range(len(self.features_known_list)):
                        e_distance_tmp = self.return_euclidean_distance(current_face_feature, self.features_known_list[i])
                        current_face_distance.append(e_distance_tmp)

                    similar_person_num = np.argmin(current_face_distance)

                    if current_face_distance[similar_person_num] < 0.4:
                        name = self.known_face_names[similar_person_num]
                        confidence = 1 - current_face_distance[similar_person_num]
                        self.response(True, name, confidence)
                        self.obj.check(self.obj.get_id(name),id)
                    else:
                        self.response(True, "unknown", current_face_distance[similar_person_num])
                        self.obj.clientDict[id].msg = ""

                self.image_processed(id)

        def start(self):
            t = threading.Thread(target=self.detect_faces)
            t.start()

        def stop(self):
            self.flagRestart = True
            print("WAITING : Detect stopped!")

        def restart(self):
            self.flagRestart = False
            print("SUCCESS : Detect restarted!")

        class Client():
            
            def __init__(self,obj,IP_ADDR,IP_PORT,Type,id):
                self.obj = obj
                self.IP_ADDR = IP_ADDR
                self.IP_PORT = IP_PORT
                self.Type = Type
                self.id = id
                self.msg=""

            def get_type(self):
                return self.Type

            def get_msg(self):
                return self.msg
            
            def start_client(self):
                t = threading.Thread(target=self.start)
                t.start()
            
            def start(self):
                msg = f"WAITING : Waiting for Connection on {self.IP_ADDR}:{self.IP_PORT}"
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
                        
                        if(self.obj.is_image_in_queue(self.id)):
                            self.obj.update_image_in_queue(self.id,image)


            # handshake with client
            async def serverRun(self, websocket):
                await self.serverHands(websocket)
                msg = f"SUCCESS : Connection start on {self.IP_ADDR}:{self.IP_PORT}"
                self.obj.obj.log.log(msg)
                print(msg)

                # self.obj.flagDetect = True
                try:
                    await self.serverRecv(websocket)
                except websockets.exceptions.ConnectionClosed:
                    # self.obj.flagDetect = False
                    msg = f"SUCCESS : Connection closed on {self.IP_ADDR}:{self.IP_PORT}"
                    self.obj.obj.log.log(msg)
                    print(msg)
                    # self.obj.obj.del_client(self.id)
                    msg = f"WAITING : Waiting for Reconnection on {self.IP_ADDR}:{self.IP_PORT}"
                    self.obj.obj.log.log(msg)
                    print(msg)

if __name__ == "__main__":
    os.system('cls')
    c = control()
    c.add_client()
    c.add_client()


