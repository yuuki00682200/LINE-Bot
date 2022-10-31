import asyncio
import random
import typing
import api
import datetime


class KickerFunction:
    def __init__(self):
        assert len(self.kicker) > 1
        self.client: api.LineClient
        self.kicker: typing.List[api.LineClient]

    async def is_test(self, msg):
        """キッカーの動作確認をします"""
        assert len(self.kicker) > 1
        task = asyncio.wait([c.sendMessage(msg.to, "ok") for c in self.kicker]) 
        await task
 
    async def is_help(self, msg):
        """説明書を出します"""
        assert len(self.kicker) > 1
        result = 'USJbot help\n\n\\\\(使用例), {注意}//\n\n'
        funcs = [f for f, c in KickerFunction.__dict__.items()]
        fnum = 0
        for func in funcs:
            if func.startswith('st') or func.startswith('is'):
                doc = getattr(KickerFunction, func).__doc__
                if doc:
                    name = func[3:]
                    result += f"k.{name} >> {doc}\n\n"
                    fnum += 1
        await self.client.sendMessage(msg.to, f"{result}\ncommands :{fnum}")
    async def st_mk(self, msg):
        """キッカーでmkします(k.mk:@mention)"""
        assert len(self.kicker) > 1
        mids = await self.client.getMidWithTag(msg)
        task = [random.choice(self.kicker).kickoutFromGroup(msg.to, mid) for mid in mids]
        await asyncio.wait(task)

    async def st_nk(self, msg):
        """キッカーでnkします(k.nk:text)"""
        assert len(self.kicker) > 1
        group = await self.client.getGroup(msg.to)
        mids = [c.mid for c in filter(lambda c:cmd in c.displayName, group.members)]
        if msg._from in mids:
            mids.remove(msg._from)
        task = [random.choice(self.kicker).kickoutFromGroup(msg.to, mid) for mid in mids]
        await asyncio.wait(task)

    async def st_ok(self, msg):
        """キッカーでokします(k.ok:text)"""
        assert len(self.kicker) > 1
        group = await self.client.getGroup(msg.to)
        mids = [c.mid for c in filter(lambda c:cmd in c.displayNameOverridden if c.displayNameOverridden is not None else False, group.members)]


        task = [random.choice(self.kicker).kickoutFromGroup(msg.to, mid) for mid in mids]
        await asyncio.wait(task)

    async def is_kickall(self, msg):
        """キッカーでkickallします"""
        assert len(self.kicker) > 1
        group = await self.client.getGroup(msg.to)
        mids = [c.mid for c in group.members]
        for mid in self.mids:
            if mid in mids:
                mids.remove(mid)
        task = [random.choice(self.kicker).kickoutFromGroup(msg.to, mid) for mid in mids]
        await asyncio.wait(task)

    async def is_gopen(self, msg):
        """キッカーでgopenします"""
        assert len(self.kicker) > 1
        group = await self.client.getGroup(msg.to)
        if group.preventedJoinByTicket:
            group.preventedJoinByTicket = False
            random.choice(self.kicker).updateGroup(group)
            await self.client.sendMessage(msg.to, "ok")

    async def is_gclose(self, msg):
        """キッカーでgcloseします"""
        assert len(self.kicker) > 1
        group = await self.client.getGroup(msg.to)
        if not group.preventedJoinByTicket:
            group.preventedJoinByTicket = True
            random.choice(self.kicker).updateGroup(group)
            await self.client.sendMessage(msg.to, "ok")
    
    async def is_join(self, msg):
        """キッカーをURLでいれます"""
        assert len(self.kicker) > 1
        group = await self.client.getGroup(msg.to)
        if group.preventedJoinByTicket:
            group.preventedJoinByTicket = False
            group.name = group.name + "\n"
            await self.client.updateGroup(group)
        ticket = await self.client.reissueGroupTicket(msg.to)
        task = [c.acceptGroupInvitationByTicket(msg.to, ticket) for c in self.kicker]
        await asyncio.wait(task)
        await self.client.sendMessage(msg.to, "ok")

    async def is_join_and_kick(self, msg):
        """キッカーを入れた瞬間破壊します"""
        assert len(self.kicker) > 1
        await self.is_join(msg)
        await self.is_kickall(msg)

    async def is_accept(self, msg):
        """招待中にいるキッカーを参加させます"""
        assert len(self.kicker) > 1
        task = [c.acceptGroupInvitation(msg.to) for c in self.kicker]
        await asyncio.wait(task)
        await self.client.sendMessage(msg.to, "ok")

    async def st_macro(self, msg):
        """キッカーでmacroします(macro:int:text)"""
        assert len(self.kicker) > 1
        cmd = msg.text.split(":")
        num = int(cmd[1])
        text = ":".join(cmd[2:])
        task = [random.choice(self.kicker).sendMessage(msg.to, text) for _ in range(num)]
        await asyncio.wait(task)

    async def is_limit(self, msg):
        """キッカーのlimit"""
        assert len(self.kicker) > 1
        result = ""
        for n, k in enumerate(self.kicker, start=1):
            try:
                await k.kickoutFromGroup(msg.to, self.mids[n])
                result += f"{n} no limit\n"
            except:
                result += f"{n} limit\n"
        await self.client.sendMessage(msg.to, result.strip())

    async def is_reset(self, msg):
        """キッカーを消します"""
        assert len(self.kicker) > 1
        self.kicker.clear()
        await self.client.sendMessage(msg.to, "ok")

    async def is_leave(self, msg):
        """キッカーを退会させます"""
        assert len(self.kicker) > 1
        task = [k.leaveGroup(msg.to) for k in self.kicker]
        await asyncio.wait(task)

    async def st_rk(self, msg):
        """指定した人数蹴ります(k.rk:int)"""
        assert len(self.kicker) > 1
        cmd = int(msg.text[5:])
        group = await self.client.getGroup(msg.to)
        mids = [con.mid for con in group.members]
        for mid in mids:
            if mid in self.mids:
                mids.remove(mid)
        task = [random.choice(self.kicker).kickoutFromGroup(msg.to, mid) for mid in mids[:cmd]]
        await asyncio.wait(task)
    
    async def is_kick(self, msg):
        """選択した人たちを蹴ります"""
        assert len(self.kicker) > 1
        task = [random.choice(self.kicker).kickoutFromGroup(msg.to, mid) for mid in self.selects]
        await asyncio.wait(task)

    async def st_name(self, msg):
        """キッカーの名前(name:str)"""
        assert len(self.kicker) > 1
        cmd = msg.text[7:]
        for k in self.kicker:
            pr = await k.getProfile()
            pr.displayName = cmd
            await k.updateProfile(pr)
        await self.client.sendMessage(msg.to, "ok")

    async def is_copy(self, msg):
        """キッカーがあれする"""
        assert len(self.kicker) > 1
        pro = await self.client.getProfile()
        task = [k.updateProfile(pro) for k in self.kicker]
        await asyncio.wait(task)

    async def st_fuck(self, msg):
        """アナウンコマクロ(fuck:int:@mention or mid)"""
        assert len(self.kicker) > 1
        cmd = msg.text.split(":")
        if msg.contentMetadata:
            mid = await self.client.getMidWithTag(msg)
            mid = mid[0]
        else:
            mid = cmd[2]
        to = msg.to
        _msg = msg
        _msg.to = mid
        task = [random.choice(self.kicker).createChatRoomAnnouncement(_msg, "fuck") for _ in range(int(cmd[1]))]
        await asyncio.wait(task)
        await self.client.sendMessage(to, "ok")

        
