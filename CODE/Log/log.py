import logging
import time
    
class log():
    def __init__(self):
        self.date=time.strftime("%Y-%m-%d", time.localtime())
        self.LogPath=f"Log/{self.date}-log.log"
        self.file = open(self.LogPath, 'a')
        self.setweblog()

        
    def setweblog(self):
        logger = logging.getLogger('werkzeug')
        handler = logging.FileHandler(f'Log/{self.date}-weblog.log')
        handler.addFilter(lambda record: 'getState' not in record.getMessage())
        logger.addHandler(handler)

    def log(self,msg):
        self.file.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " " + msg )