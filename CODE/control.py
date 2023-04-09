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
        
    def time(self):
        nowdate=time.strftime('%Y-%m-%d',time.localtime())
        nowtime=time.strftime('%H:%M:%S',time.localtime())
        return nowdate,nowtime

    def renew_status(self):
        for i in list(self.info.keys()):
            self.user_status[i]=bool(list(self.database.get_newest_data('entry',i))[0][-1])

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

    def addface(self):
        userid=list(self.info.keys())[-1]+1
        print(userid)
        addface.addface(userid)
    
    def updatefaceinfo(self,userid,name,email):
        info=[userid,name,email]
        self.database.add_entry('info',info)


# print(addface.addface())
if __name__ == "__main__":
    os.system('cls')
    c=control()
    c.addface()