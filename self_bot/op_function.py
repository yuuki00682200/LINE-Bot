from .command_check import CommandCheck
from line_api.TalkService import ttypes
from .text_conv import TextConv
import asyncio
import api

class OpFunction(CommandCheck):
    def __init__(self):
        self.client: api.LineClient
        CommandCheck.__init__(self)

    def op_check(self, op, type):
        return op.type == type

    def check_content_type(self, msg, type):
        return msg.contentType == type

    async def send_message(self, op):
        msg = op.message
        if self.mids[0] != msg._from:
            await self.client.sendMessage(msg.to, "IDが一致してません")
            return await self.client.client.logout(self.client.context)
        if self.check_content_type(msg, ttypes.ContentType.CONTACT):
            await self.client.sendMessage(op.message.to, msg.contentMetadata["mid"])
        command = self.is_command(msg.text)
        if command:
            await command(self, msg)

    async def receive_message(self, op):
        msg = op.message
        if self.check_content_type(msg, ttypes.ContentType.CONTACT):
            self.contact = msg.contentMetadata["mid"]
        elif self.check_content_type(msg, ttypes.ContentType.NONE):
            if msg.to in self.data["group"] or self.data["auto"]["read"]:
                await self.client.sendChatChecked(msg.to, msg.id)

    async def add_contact(self, op):
        if self.data["auto"]["add"]:
            await self.client.findAndAddContactsByMid(op.param1)

    async def leave_room(self, op):
        if self.data["auto"]["leave"]:
            await self.client.leaveRoom(op.param1)

    async def invite_into_group(self, op):
        if self.data["auto"]["join"]:
            await self.client.acceptGroupInvitation(op.param1)

    async def accept_group_invitation(self, op):
        if self.data["auto"]["greeting"] or op.param1 in self.data["group"]["greeting"]:
            await self.client.sendMessage(op.param1, TextConv(self.client, op, self.data["text"]["greeting"]).text)

    async def kickout_from_group(self, op):
        if op.param1 in self.data["group"]["kick"]:
            if op.param2 in self.mids:
                return
            if op.param3 not in self.mids:
                return
            print("kick")
            if len(self.mids) > 1:
                index = self.mids.index(op.param3) - 1
                if index == len(self.kicker):
                    _index = index - 1
                else:
                    _index = index + 1
                await self.kicker[_index].kickoutFromGroup(op.param1, op.param2)
                list_ = [self.client] + self.kicker
                ticket = await self.kicker[_index].reissueGroupTicket(op.param1)
                group = await self.client.getGroup(op.param1)
                if group.preventedJoinByTicket:
                    group.preventedJoinByTicket = False
                    await self.kicker[_index].updateGroup(group)
                task = [c.acceptGroupInvitationByTicket(op.param1, ticket) for c in list_]
                await asyncio.wait(task)


    async def unsend_message(self, op):
        if self.data["auto"]["restore"] or op.param1 in self.data["group"]["restore"]:
            if op.param2 in self.message:
                con = await self.client.getContact(self.message[op.param2]._from)
                await self.client.sendMessage(op.param1, f"{con.displayName}\n\n{self.message[op.param2].text}")

