import logging
import time
    
class log():
    def __init__(self):
        self.date=time.strftime("%Y-%m-%d", time.localtime())
        self.LogPath=f"Log/{self.date}-log.log"
        self.file = open(self.LogPath, 'a', encoding="utf-8")

        self.setweblog()

        
    def setweblog(self):
        logger = logging.getLogger('werkzeug')
        handler = logging.FileHandler(f'Log/{self.date}-weblog.log',encoding="utf-8")
        handler.addFilter(lambda record: 'getState' not in record.getMessage())
        handler.addFilter(lambda record: '/static' not in record.getMessage())
        logger.addHandler(handler)

    def log(self,msg):
        self.file.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " " + msg +"\n")
        self.file.flush()

if __name__ == '__main__':
    log=log()
    log.log("test")