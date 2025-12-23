from linebot.generated.line_api.TalkService.ttypes import OpType
from .op_function import OpFunction


class Run(OpFunction):
    def __init__(self):
        self.contact = None
        OpFunction.__init__(self)

    async def run(self, op):
        if self.op_check(op, OpType.RECEIVE_MESSAGE):
            await self.receive_message(op)

        elif self.op_check(op, OpType.SEND_MESSAGE):
            await self.send_message(op)

        elif self.op_check(op, OpType.NOTIFIED_ADD_CONTACT):
            await self.add_contact(op)

        elif self.op_check(op, OpType.NOTIFIED_INVITE_INTO_ROOM):
            await self.leave_room(op)

        elif self.op_check(op, OpType.NOTIFIED_INVITE_INTO_GROUP):
            await self.invite_into_group(op)

        elif self.op_check(op, OpType.NOTIFIED_ACCEPT_GROUP_INVITATION):
            await self.accept_group_invitation(op)

        elif self.op_check(op, OpType.NOTIFIED_DESTROY_MESSAGE):
            await self.unsend_message(op)

        elif self.op_check(op, OpType.NOTIFIED_KICKOUT_FROM_GROUP):
            await self.kickout_from_group(op)

