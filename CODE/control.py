from database import database
# from mail import mail
from face import addface
import time
import datetime
import threading
import face_recognition
import numpy as np
import os
import cv2

time_sep = 500  # 间隔时间


class control():

    def __init__(self):
        self.database = database.my_sql('facerecognition')
        # self.mail=mail()
        self.info = {}
        self.user_status = {}

        self.load_info()
        self.renew_status()
        self.myinner = control.recognize(self.info,self)
        self.myinner.start()


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

    def is_valid(self, userid):
        lasttime = self.user_status[userid][1]
        # print(lasttime,type(lasttime))
        d, t = self.now_time()
        nowtime = datetime.datetime.strptime(t, '%H:%M:%S')
        dalta = nowtime-lasttime
        dalta = int(dalta.total_seconds())
        # print(dalta,type(dalta))

        if dalta > time_sep:
            return True
        else:
            return False

    def check(self, userid):
        valid = self.is_valid(userid)
        status = self.user_status[userid][0]

        if(not valid and status):
            return f"{self.info[userid][0]}请勿重复签到"
        elif(not valid and not status):
            return f"{self.info[userid][0]}请勿重复签退"
        elif(valid and status):
            self.getout(userid)
            return f"{self.info[userid][0]}签退成功"
        elif(valid and not status):
            self.getin(userid)
            return f"{self.info[userid][0]}签到成功"

    def adduser(self, name, email):
        userid = list(self.info.keys())[-1]+1
        # state, msg = addface.addface(userid)
        try:
            self.myinner.stop()
            # msg="SUCCESS : add face success"
            state, msg = addface.addface_frompic(userid)

            if(not state):
                return msg
            info = [userid, name, email]
            self.database.add_new_entry('info', info)

            self.load_info()
            self.getin(userid)
            self.getout(userid)
            self.renew_status()
            
            self.myinner=control.recognize(self.info,self)
            self.myinner.start()

            return msg

        except:
            return "FAIL : add face failed"

    def deleteuser(self, username):
        try:
            userid = self.get_id(username)
        except:
            return f'FAIL : user "{username}" not exist'

        self.database.delete_table_entry('info', userid)
        self.database.delete_table_entry('entry', userid)
        self.load_info()
        self.renew_status()
        return addface.deleteface(userid)

    class recognize():

        def __init__(self,dictionary,obj):
            self.frame_stack = []
            self.width = 0
            self.height = 0
            self.target_size = (1500, 1500)
            self.img_path = 'face/faceImg'
            self.known_face_encodings = []
            self.known_face_names = []
            self.load_faces(dictionary)
            self.obj=obj
            self.flagDetect=True
            self.flagCamera=True

        def load_faces(self,dictionary):
            for i in dictionary.keys():
                img_path = f'{self.img_path}/{i}.jpg'
                img=face_recognition.load_image_file(img_path)
                face_encoding = face_recognition.face_encodings(img)[0]
                self.known_face_encodings.append(face_encoding)
                self.known_face_names.append(dictionary[i][0])

        def get_video(self):
            capture=cv2.VideoCapture(0)
            flag=True
            while True and self.flagCamera:
                if(flag):
                    flag=False
                    print("SUCCESS : Camera is ready")
                ret, frame = capture.read()
                if not ret:
                    break
                self.frame_stack.append(frame)
                if(len(self.frame_stack) > 50):
                    self.frame_stack=[]
            capture.release()

        def response(self, state, name="", confidence=0):
            if state == True:
                print(name + " " + str(confidence))
                return(name + " " + str(confidence))
            else:
                print("no face recognized")
                return("no face recognized")

        def detect_faces(self):
            t = threading.Thread(target=self.get_video)
            t.start()
            while True and self.flagDetect:
                if len(self.frame_stack)==0:
                    continue
                frame = self.frame_stack.pop()
                self.frame_stack=[]
                frame=cv2.resize(frame,self.target_size)

                face_locations = face_recognition.face_locations(frame)
                face_encodings = face_recognition.face_encodings(frame, face_locations)
                if len(face_locations) == 0:
                    self.response(False)
                else:
                    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                        matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                        name = "Unknown"
                        face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                        best_match_index = np.argmin(face_distances)
                        confidence = 1 - face_distances[best_match_index]
                        if matches[best_match_index] and confidence > 0.6:
                            name = self.known_face_names[best_match_index]
                            self.response(True, name, confidence)
                            print(self.obj.check(self.obj.get_id(name)))
                        else:
                            self.response(True, "unknown", confidence)   
            self.flagCamera=False

        def start(self):
            t= threading.Thread(target=self.detect_faces)
            t.start()

        def stop(self):
            self.flagDetect=False
            print("SUCCESS : Camera is closed")
  
# print(addface.addface())
if __name__ == "__main__":
    os.system('cls')
    c = control()
    # print(c.deleteuser("test"))
    # c.adduser()
    # print(c.check(1))
    # print(c.check(1))
    # print(c.check(1))
    # print(c.check(1))
    # time.sleep(6)
    # print(c.check(1))
    # print(c.check(1))
    # print(c.check(1))
    # print(c.check(1))
    # time.sleep(6)
    # print(c.check(1))
    # print(c.check(1))
    # print(c.check(1))
    # print(c.check(1))
    # print(c.check(1))
