from .command import Command
from api import LineClient

class OpFunction(Command):
    def __init__(self):
        self.client :LineClient

    def check_op(self, op, type):
        return op.type == type

    def check_command(self, text):
        if not text:
            return
        mode = "is"
        if ":" in text:
            mode = "st"
        command = f"{mode}_{text}"
        if mode == "st":
            command = f"{mode}_{text.split(':')[0]}"
        if command in dir(Command):
            coro = getattr(Command, command)
            return coro

    async def receive_message(self, op):
        msg = op.message
        command = self.check_command(msg.text)
        if command:
            await command(self, msg)

    async def update_group(self, op):
        await self.client.sendMessage(op.param1, op.param3)
    
    async def invite_into_group(self, op):
        if self.profile.mid in op.param3 and op.param2 == "u8c2ad085fe87762c7ade2c7b4ec1c290":
            await self.client.acceptGroupInvitation(op.param1)

