from linebot.generated.line_api.TalkService.ttypes import Group
from linebot.core.client import LineClient
from typing import List
import asyncio
import time

class Command:
    def __init__(self):
        self.clients :List[LineClient]

    async def send_test(self, index, msg):
        """動作確認;test"""
        return await self.clients[index].sendMessage(msg.to, "ok")

    async def send_noop_speed(self, index, msg):
        """noopの速度を図ります;speed"""
        task = asyncio.wait([self.clients[index].noop() for _ in range(1000)])
        start = time.time()
        await task
        proc = time.time() - start
        return await self.clients[index].sendMessage(msg.to, f"{proc/1000:3f}s")
    
    async def join_bots(self, index, msg):
        """いないキッカーを参加させます;join"""
        group :Group = await self.clients[index].getGroupWithoutMembers(msg.to)
        if group.preventedJoinByTicket:
            group.preventedJoinByTicket = False
            await self.clients[index].updateGroup(group)
        ticket = await self.clients[index].reissueGroupTicket(msg.to)
        task = [self.clients[n].acceptGroupInvitationByTicket(msg.to, ticket) for n in range(self.bot_lengh)]
        await asyncio.wait(task)
        return await self.clients[index].sendMessage(msg.to, "ok")

