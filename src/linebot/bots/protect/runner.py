from linebot.generated.f_line_api.TalkService.ttypes import (
    OpType, 
    Operation, 
    Message,
    ContentType,
    Group
)
from .command import Command
#from .main import Protect
import asyncio
import random
import time

#class Runner(Protect):
class Runner(Command):
    def __init__(self):
        self.__invite_protect = {}
        Command.__init__(self)

    def is_admin(self, op_or_message):
        if isinstance(op_or_message, Operation):
            return op_or_message.param2 in self.user_data["user"]["admin"]
        elif isinstance(op_or_message, Message):
            return op_or_message._from in self.user_data["user"]["admin"]
        return False

    def is_bot(self, op, param_number):
        if param_number == 1:
            return op.param1 in self.bot_mids
        elif param_number == 2:
            return op.param2 in self.bot_mids
        elif param_number == 3:
            return op.param3 in self.bot_mids

    def is_pass_mid(self, op):
        return self.is_admin(op) or self.is_white_list(op) or self.is_bot(op, 2)

    def is_white_list(self, op):
        return op.param2 in self.user_data["user"]["white"]
    
    def is_black_list(self, op_or_message):
        if isinstance(op_or_message, Operation):
            return op_or_message.param2 in self.user_data["user"]["black"]
        elif isinstance(op_or_message, Message):
            return op_or_message._from in self.user_data["user"]["black"]
        return False

    def is_protected(self, op_or_message, obj):
        if isinstance(op_or_message, Operation):
            return op_or_message.param1 in self.user_data["group"][obj]
        elif isinstance(op_or_message, Message):
            return op_or_message.to in self.user_data["group"][obj]
        

    async def run(self, op):
        op :Operation
        if op.type == OpType.RECEIVE_MESSAGE:
            await self.__receive_message(op)
        
        elif op.type == OpType.NOTIFIED_INVITE_INTO_GROUP:
            await self.__invite_into_group(op)

        elif op.type == OpType.NOTIFIED_ACCEPT_GROUP_INVITATION:
            await self.__accept_group(op)

        elif op.type == OpType.NOTIFIED_KICKOUT_FROM_GROUP:
            await self.__kickout_from_group(op)

        elif op.type == OpType.NOTIFIED_UPDATE_GROUP:
            await self.__update_group(op)
            
    async def __receive_message(self, op):
        prefix = None
        if op.message.contentType == ContentType.CONTACT:
            mid = op.message.contentMetadata["mid"]
            op.message.text = "/user:" + mid
            coroutine, prefix = self.command_handler.get_command(f"/user:{mid}")
        is_admin = self.is_admin(op.message)
        if is_admin:
            if not prefix:
                coroutine, prefix = self.command_handler.get_command(op.message.text)
            if coroutine:
                op.message.text = op.message.text[len(prefix):]
                return await coroutine(self, op.message)
        elif self.is_black_list(op):
            await random.choice(self.clients[1:]).kickoutFromGroup(op.message.to, op.message._from)

    async def __update_group(self, op):
        if self.is_protected(op, "url"):
            if not self.is_pass_mid(op):
                if op.param3 in {"4", "5", "6", "7"}:
                    group = await random.choice(self.clients[1:]).getGroupWithoutMembers(op.param1)
                    if not group.preventedJoinByTicket:
                        await random.choice(self.clients[1:]).kickoutFromGroup(op.param1, op.param2)
                        group.preventedJoinByTicket = True
                        await random.choice(self.clients[1:]).updateGroup(group)

    async def __kickout_from_group(self, op):
        if self.is_black_list(op):
            task = [random.choice(self.clients[1:]).kickoutFromGroup(op.param1, mid) for mid in self.temp_black]
            await asyncio.wait(task)
        if self.is_protected(op, "kick"):
            if not self.is_pass_mid(op):
                await random.choice(self.clients[1:]).kickoutFromGroup(op.param1, op.param2)
        if op.param3 in self.user_data["user"]["admin"]:
            if not self.is_pass_mid(op):
                await random.choice(self.clients[1:]).kickoutFromGroup(op.param1, op.param2)
                await self.clients[0].findAndAddContactsByMid(op.param1)
                await self.clients[0].inviteIntoGroup(op.param1, [op.param3])

        if self.is_bot(op, 3) and not self.is_pass_mid(op):
            index = self.bot_mids.index(op.param3)
            if index == self.bot_length:
                index -= 1
            else:
                index += 1
            self.temp_black.append(op.param2)
            group = await self.clients[index].getGroupWithoutMembers(op.param1)
            ticket = await self.clients[index].reissueGroupTicket(op.param1)
            task = [self.clients[index].kickoutFromGroup(op.param1, mid) for mid in self.temp_black]
            if group.preventedJoinByTicket:
                task.append(self.__open_gticket(group, index))
            await asyncio.wait(task)
            task = [self.clients[n].acceptGroupInvitationByTicket(op.param1, ticket) for n in range(self.bot_length-1)]
            return await asyncio.wait(task)

    async def __open_gticket(self, group, index):
            group.preventedJoinByTicket = False
            await self.clients[index].updateGroup(group)
            
    async def __accept_group(self, op):
        if self.is_black_list(op):
            await random.choice(self.clients[1:]).kickoutFromGroup(op.param1, op.param2)
        if self.is_protected(op, "join"):
            if not self.is_pass_mid(op):
                await random.choice(self.clients[1:]).kickoutFromGroup(op.param1, op.param2)
        if op.param1 in self.__invite_protect:
            if not self.is_pass_mid(op):
                if time.time() - self.__invite_protect[op.param1] < 2:
                    await self.clients[0].kickoutFromGroup(op.param1, op.param2)
                    self.__invite_protect.pop(op.param1)

    async def __invite_into_group(self, op):
        if self.is_bot(op, 3):
            if self.is_admin(op):
                await self.clients[0].acceptGroupInvitation(op.param1)
        elif self.is_protected(op, "invite"):
            if not self.is_pass_mid(op):
                self.__invite_protect[op.param1] = time.time()
                await random.choice(self.clients[1:]).cancelGroupInvitation(op.param1, op.param3)
            

