from linebot.generated.line_api.TalkService.ttypes import OpType
from .op_function import OpFunction


class Run(OpFunction):
    def __init__(self):
        OpFunction.__init__(self)
    
    async def run(self, op):
        if self.check_op(op, OpType.RECEIVE_MESSAGE):
            await self.receive_message(op)

        elif self.check_op(op, OpType.NOTIFIED_INVITE_INTO_GROUP):
            await self.invite_into_group(op)

        elif self.check_op(op, OpType.NOTIFIED_UPDATE_GROUP):
            await self.update_group(op)
