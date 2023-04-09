from database import database
# from mail import mail
from face import addface
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
        print(list(self.info.keys()))
        
    
    def renew_status(self):
        for i in list(self.info.keys()):
            self.user_status[i]=bool(list(self.database.get_newest_data('entry',i))[0][-1])
        print(self.user_status)



# print(addface.addface())
if __name__ == "__main__":
    os.system('cls')
    c=control()