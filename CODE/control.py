from database import database
# from mail import mail
from face import addface
import time
import threading
import os

class control():
    def __init__(self):
        self.database=database.my_sql('facerecognition')
        # self.mail=mail()
        self.info={}
        self.user_status={}

        self.load_info()
        self.renew_status()

    def load_info(self):
        l=list(self.database.get_all_data('info'))
        for i in l:
            self.info[i[0]]=[i[1],i[2]]
        # print(list(self.info.keys()))
        
    def time(self):
        nowdate=time.strftime('%Y-%m-%d',time.localtime())
        nowtime=time.strftime('%H:%M:%S',time.localtime())
        return nowdate,nowtime

    def renew_status(self):
        for i in list(self.info.keys()):
            self.user_status[i]=bool(list(self.database.get_newest_data('entry',i))[0][-1])
        # print(self.user_status)

    def getin(self,userid):
        d,t=self.time()
        entry=[userid,self.info[userid][0],d,t,'',True]
        self.database.add_entry('entry', entry)
        self.renew_status()

    def getout(self,userid):
        d,t=self.time()
        self.database.update_entry(userid,t)
        self.renew_status()

    def check(self,userid):
        if self.user_status[userid]:
            self.getout(userid)
        else:
            self.getin(userid)


# print(addface.addface())
if __name__ == "__main__":
    os.system('cls')
    c=control()
    c.check(1)
    time.sleep(5)
    c.check(1)