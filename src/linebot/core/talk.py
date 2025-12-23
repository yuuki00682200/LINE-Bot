from linebot.generated.f_line_api.TalkService import ttypes, f_TalkService
import random


class Talk:
    def __init__(self):
        self.client: f_TalkService.Client

    async def noop(self):
        return await self.client.noop(self.context)

    async def getServerTime(self):
        return await self.client.getServerTime(self.context)

    async def findContactByUserid(self, id):
        return await self.client.findContactByUserid(self.context, [id])

    async def getBlockedContactIds(self):
        return await self.client.getBlockedContactIds(self.context)

    async def createGroup(self, name, ids):
        return await self.client.createGroup(self.context, 1, name, ids)

    async def getProfile(self):
        return await self.client.getProfile(self.context)

    async def getSettings(self):
        return await self.client.getSettings(self.context)

    async def updateProfile(self, profile):
        return await self.client.updateProfile(self.context, 0, profile)

    async def getLastOpRevision(self, poll=True):
        if poll:
            return await self.poll.getLastOpRevision(self.context)
        return await self.client.getLastOpRevision(self.context)
        

    async def fetchOperations(self, rev, count):
        return await self.poll.fetchOperations(self.context, rev, count)

    async def fetchOps(self, rev, count):
        return await self.poll.fetchOps(self.context, rev, count, 0, 0)

    async def getContact(self, mid):
        return await self.client.getContact(self.context, mid)

    async def getContacts(self, mids):
        return await self.client.getContacts(self.context, mids)

    async def sendMessage(self, to, text):
        msg = ttypes.Message(to=to, text=text, contentMetadata={'NOTIFICATION_DISABLED': 'true', 'BOT_CHECK': '1', 'BOT_TRACK': 'api=re'})
        #msg = ttypes.Message(to=to, text=text)
        return await self.client.sendMessage(self.context, 0, msg)

    async def sendContact(self, to, mid):
        msg = ttypes.Message(
            to=to,
            text='',
            contentMetadata={'mid': mid},
            contentType=ttypes.ContentType.CONTACT)
        return await self.client.sendMessage(self.context, 0, msg)

    async def sendChatChecked(self, gid, id):
        return await self.client.sendChatChecked(self.context, 0, gid, id, random.randint(0, 10))

    async def getMidWithTag(self, msg):
        if msg.contentMetadata:
            if not "MENTION" in msg.contentMetadata:
                return
            result = []
            key = eval(msg.contentMetadata['MENTION'])
            for mid in key['MENTIONEES']:
                result.append(mid['M'])
            return result

    async def updateContactSetting(self, mid, attr, value):
        return await self.client.updateContactSetting(self.context, 0, mid, attr, value)

    async def updateContactName(self, mid, string):
        return await self.updateContactSetting(mid, 2, string)

    async def findAndAddContactsByMid(self, mid):
        return await self.client.findAndAddContactsByMid(self.context, 0, mid, 0, '')

    async def leaveRoom(self, gid):
        return await self.client.leaveRoom(self.context, 0, gid)

    async def getGroup(self, gid):
        return await self.client.getGroup(self.context, gid)
    
    async def getGroups(self, gids):
        return await self.client.getGroups(self.context, gids)


    async def getGroupWithoutMembers(self, gid):
        return await self.client.getGroupWithoutMembers(self.context, gid)

    async def reissueGroupTicket(self, gid):
        return await self.client.reissueGroupTicket(self.context, gid)

    async def updateGroup(self, group):
        return await self.client.updateGroup(self.context, 0, group)

    async def kickoutFromGroup(self, gid, mid):
        return await self.client.kickoutFromGroup(self.context, 0, gid, [mid])

    async def acceptGroupInvitation(self, gid):
        return await self.client.acceptGroupInvitation(self.context, 0, gid)

    async def acceptGroupInvitationByTicket(self, gid, ticket):
        return await self.client.acceptGroupInvitationByTicket(self.context, 0, gid, ticket)

    async def inviteIntoGroup(self, gid, midlist):
        return await self.client.inviteIntoGroup(self.context, 0, gid, midlist)

    async def leaveGroup(self, gid):
        return await self.client.leaveGroup(self.context, 0, gid)

    async def createRoom(self, mids):
        return await self.client.createRoom(self.context, 0, mids)

    async def getGroupIdsJoined(self):
        return await self.client.getGroupIdsJoined(self.context)

    async def getGroupIdsInvited(self):
        return await self.client.getGroupIdsInvited(self.context)

    async def getAllContactIds(self):
        return await self.client.getAllContactIds(self.context)

    async def getBlockedContactIds(self):
        return await self.client.getBlockedContactIds(self.context)

    async def blockContact(self, mid):
        return await self.client.blockContact(self.context, 0, mid)

    async def unblockContact(self, mid):
        return await self.client.unblockContact(self.context, 0, mid)

    async def cancelGroupInvitation(self, gid, mid):
        return await self.client.cancelGroupInvitation(self.context, 0, gid, [mid])

    async def updateSettingsAttribute(self, a, b, c):
        return await self.client.updateSettingsAttribute(self.context, a, b, c)

    async def createChatRoomAnnouncement(self, msg, text):
        content = ttypes.ChatRoomAnnouncementContents(
            displayFields=11,
            text=text,
            link=f"line://nv/chatMsg?chatId={msg.to}&messageId={msg.id}")
        return await self.client.createChatRoomAnnouncement(self.context, 1, msg.to, 0, content)

