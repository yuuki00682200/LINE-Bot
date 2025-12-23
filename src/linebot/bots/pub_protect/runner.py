from linebot.generated.line_api.TalkService.ttypes import OpType
from .op_handler import (
        receive_message
)

class Runner(receive_message.ReceiveMessage):
    def __init__(self):
        receive_message.ReceiveMessage.__init__(self)

    def op_handler(self, op, type):
        return op.type == type

    async def run(self, index, op):
        if self.op_handler(op, OpType.RECEIVE_MESSAGE):
            return await self.receive_message(index, op)

