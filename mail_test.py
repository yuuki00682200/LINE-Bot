import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate

def create_message(from_addr, to_addr, subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_addr
    msg['To'] = to_addr
    return msg


def send_mail(body_msg):
    smtpobj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpobj.ehlo()
    smtpobj.starttls()
    smtpobj.ehlo()
    smtpobj.login("@gmail.com", "usermode")
    a = smtpobj.sendmail(body_msg["From"], body_msg["To"], body_msg.as_string())
    smtpobj.close()

body = create_message("kotabbcc@gmail", "kouta_19n1101637@nnn.ed.jp", "Test", "test")
send_mail(body)
