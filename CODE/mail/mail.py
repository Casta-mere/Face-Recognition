import time
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


class email():
    
    def __init__(self):
        self.email_host = 'smtp.qq.com'
        self.email_user = '2287245796@qq.com'
        self.email_certificate = 'dxxqtwfuokjbdjjf'
        self.email_sender = '2287245796@qq.com'

    def Send_email(self, receiver_email, receiver_name, title, text, attachment):
        message = MIMEMultipart('related')
        message['From'] = Header("Castamere", 'utf-8')
        message['To'] = Header(receiver_name, 'utf-8')
        message['Subject'] = Header(title, 'utf-8')

        att = MIMEApplication(open(attachment, 'rb').read(), 'utf-8')
        att.add_header('Content-Disposition',
                       'attachment', filename='data.csv')
        message.attach(att)

        message.attach(MIMEText(text, "html", "utf-8"))

        try:
            smtpObj = smtplib.SMTP()
            smtpObj.connect(self.email_host, 25)
            smtpObj.login(self.email_user, self.email_certificate)
            smtpObj.sendmail(self.email_sender,
                             receiver_email, message.as_string())
            print("Send success")
        except smtplib.SMTPException:

            print("Send falied")


if __name__ == '__main__':
    receiver_email = '2287245796@qq.com'
    receiver_name = '王旭刚'
    present_time = time.strftime(
        "%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    text = f'Dear Castamere \n \n In {present_time}, an Alert in your house has been triggered, please check it out on www.castamerego.com/surveillance'
    e = email()
    e.Send_email(receiver_email, receiver_name,
                 'Check!', text, "CODE\email\data.csv")
