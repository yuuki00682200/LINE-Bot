from ..command_parser.command_parser import CommandParser

class ReceiveMessage(CommandParser):
    def __init__(self):
        CommandParser.__init__(self)

    async def __get_index(self, msg):
        group = await self.clients[0].getGroup(msg.to)
        mids = [c.mid for c in group.members]
        for mid in self.mids:
            if mid in mids:
                return self.mids.index(mid)

    async def receive_message(self, index, op):
        msg = op.message
        if msg.text:
            _index = await self.__get_index(msg)
            command, pre = self.get_command(msg.text)
        if _index == index:
            if command:
                await command(self, index, msg)

