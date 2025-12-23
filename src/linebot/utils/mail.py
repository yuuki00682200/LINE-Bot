import smtplib
from email.mime.text import MIMEText
from typing import Optional

def create_message(from_addr: str, to_addr: str, subject: str, body: str) -> MIMEText:
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_addr
    msg['To'] = to_addr
    return msg

def send_mail(body_msg: MIMEText, smtp_user: str, smtp_pass: str, smtp_host: str = 'smtp.gmail.com', smtp_port: int = 587) -> None:
    smtpobj = smtplib.SMTP(smtp_host, smtp_port)
    smtpobj.ehlo()
    smtpobj.starttls()
    smtpobj.ehlo()
    smtpobj.login(smtp_user, smtp_pass)
    smtpobj.sendmail(body_msg["From"], body_msg["To"], body_msg.as_string())
    smtpobj.close()
