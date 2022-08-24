from aiohttp.client import ClientSession
from self_bot import Selfbot
from api import LineClient
from line_api.TalkService.ttypes import Settings
import asyncio
import aiohttp
import json
import sys
import os
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
    smtpobj.login("kotabbcc@gmail.com", "ogujasfcztsktiur")
    a = smtpobj.sendmail(body_msg["From"], body_msg["To"], body_msg.as_string())
    smtpobj.close()

def write_file(qr):
    os.system("rm qr_code.txt")
    if os.path.isfile("qr_code.txt"):
        os.remove("qr_code.txt")
    with open("qr_code.txt", "w") as f:
        print(qr)
        f.write(qr)

def send_pin(pin):
    body = create_message("kotabbcc@gmail", sys.argv[2], "Test", pin)
    send_mail(body)

con = aiohttp.ClientSession()
client = LineClient(
        callback=write_file,
        callback2=send_pin,
        cert=sys.argv[1],
        connector=con
    )
sb = Selfbot(client, con, sys.argv[1])
sb.main()

