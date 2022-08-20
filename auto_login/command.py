from .web_script import Web
from api import LineClient
import subprocess
import requests
import asyncio
import json
import time
import bs4
import os

class Command:
    def __init__(self):
        self.client: LineClient

    async def is_test(self, msg):
        await self.client.sendMessage(msg.to, "ok")

    async def st_red(self, msg):
        cmd = msg.text[4:]
        web = Web()
        res = web.get_red(cmd)
        result = f"分布図\n" + \
                 f"{res}\n" + \
                 f"表\n" + \
                 f"{web.host}{web.rdblist}"
        await self.client.sendMessage(msg.to, result)

    async def st_list(self, msg):
        cmd = msg.text[5:]
        web = Web()
        res = web.get_red_list(cmd)
        result = "\n\n".join([f"{k} : {v}" for k,v in dict(res).items()])
        await self.client.sendMessage(msg.to, result)

    async def is_aleave(self, msg):
        gids = await self.client.getGroupIdsJoined()
        task = [self.client.leaveGroup(gid) for gid in gids]
        await asyncio.wait(task)

    async def is_reboot(self, msg):
        await self.client.sendMessage(msg.to, "wait")
        os.execvp("python3", ["python3", "loginbot.py"])

    async def st_sign(self, msg):
        with open(self.mails, "r") as f:
            dick = json.load(f)
        if msg._from in dick:
            return
        cmd = msg.text.split(":")
        dick[msg._from] = (cmd[1], "a")
        with open(self.mails, "w") as f:
            json.dump(dick, f)
        await self.client.sendMessage(msg.to ,"ok")

    async def is_del(self, msg):
        with open(self.mails, "r") as f:
            dick = json.load(f)
        if msg._from not in dick:
            return
        dick.pop(msg._from)
        with open(self.mails, "w") as f:
            json.dump(dick, f)
        await self.client.sendMessage(msg._from ,"ok")

    async def is_login(self, msg):
        with open(self.mails, "r") as f:
            dick = json.load(f)
        if msg._from in dick:
            mail, passwd = dick[msg._from]
        else:
            await self.client.sendMessage(msg.to, "登録してください")
        subprocess.Popen(["python3", "selfbot.py", msg._from, mail, passwd])
        return await self.client.sendMessage(msg.to ,"ok")

    async def is_qr_login(self, msg):
        start = time.time()
        with open(self.mails, "r") as f:
            dick = json.load(f)
        if msg._from in dick:
            mail, passwd = dick[msg._from]
        else:
            return await self.client.sendMessage(msg.to, "登録してください")
        subprocess.run(["rm", "qr_code.txt"])
        subprocess.Popen(["python3", "selfbot_qr.py", msg._from, mail])
        while time.time() - start < 30:
            if os.path.isfile("qr_code.txt"):
                with open("qr_code.txt", "r") as f:
                    url = f.read()
                await self.client.sendMessage(msg.to, "登録したメアドに届くよ")
                await self.client.sendMessage(msg.to, url)
                break



    async def is___protect__(self, msg):
        subprocess.Popen(["python3", "protect.py", msg._from])
        await self.client.sendMessage(msg.to, "ok")

