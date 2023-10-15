import os, json
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

class Sender:
    my_sender = ""
    my_name = ""
    my_passwd = ""
    my_receiver = ""

    def __init__(self) -> None:
        current_path=os.path.split(os.path.realpath(__file__))[0]
        with open(os.path.join(current_path, f"config/mail.json")) as f:
            myconfig=json.load(f)
            self.my_sender = myconfig["sender"]
            self.my_name = myconfig["name"]
            self.my_passwd = myconfig["password"]
            self.my_receiver = myconfig["receiver"]


    def SendMail(self):
        try:
            msg = MIMEText("这是一封测试邮件","plain","utf-8")
            msg["From"] = formataddr([self.my_name,self.my_sender])
            msg["To"] = self.my_receiver #formataddr("")
            msg["Subject"] = "周报测试邮件"

            server = smtplib.SMTP_SSL("smtp.exmail.qq.com", 465)
            server.login(self.my_sender, self.my_passwd)
            server.sendmail(self.my_sender, self.my_receiver,msg.as_string())
            server.quit()
        except Exception as e:
            print("邮件发送失败")
            print(e)

    def GenContext(self):
        #参考https://blog.csdn.net/cyan_grey/article/details/108979180