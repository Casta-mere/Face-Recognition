from database import database
from email import mail
import threading


class control():
    def __init__(self):
        self.database=database.my_sql('facerecognition')
        self.mail=mail()

    