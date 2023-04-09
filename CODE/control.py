from database import database
# from mail import mail
from face import addface
import time
import datetime
import threading
import os

time_sep = 500  # 间隔时间


class control():

    def __init__(self):
        self.database = database.my_sql('facerecognition')
        # self.mail=mail()
        self.info = {}
        self.user_status = {}

        self.load_info()
        self.renew_status()

    def load_info(self):
        l = list(self.database.get_all_data('info'))
        for i in l:
            self.info[i[0]] = [i[1], i[2]]

    def now_time(self):
        nowdate = time.strftime('%Y-%m-%d', time.localtime())
        nowtime = time.strftime('%H:%M:%S', time.localtime())
        return nowdate, nowtime

    def renew_status(self):
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
        self.database.add_entry('entry', entry)
        self.renew_status()

    def getout(self, userid):
        d, t = self.now_time()
        self.database.update_entry(userid, t)
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

    def addface(self):
        userid = list(self.info.keys())[-1]+1
        print(userid)
        addface.addface(userid)

    def updatefaceinfo(self, userid, name, email):
        info = [userid, name, email]
        self.database.add_entry('info', info)


# print(addface.addface())
if __name__ == "__main__":
    os.system('cls')
    c = control()
    # c.addface()
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
