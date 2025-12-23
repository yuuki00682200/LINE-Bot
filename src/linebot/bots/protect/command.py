from api import LineClient
from typing import List
import asyncio
import random
import time
import sys
import os

class Command:
    def __init__(self):
        self.clients :List[LineClient]

    def __create_help_message(self):
        coroutines = filter(lambda x:x[:2]!="__", dir(Command))
        coroutines = [getattr(Command, coro) for coro in coroutines]
        result = "USJ仮保護bot help\n\n"
        for coro in coroutines:
            if coro.__doc__:
                doc = coro.__doc__.split(";")
                result += f"{doc[1]}\n>>> {doc[0]}\n\n"
        return result.strip()

    async def send_test(self, msg):
        """動作確認します;test, テスト"""
        return await self.clients[0].sendMessage(msg.to, "ok")

    async def send_help(self, msg):
        """説明書を送信します;help, ヘルプ"""
        return await self.clients[0].sendMessage(msg.to, self.__create_help_message())

    async def send_noop_speed(self, msg):
        """noopの速度を計測します;speed, 計測, speed:, 計測"""
        cmd = 1000
        if ":" in msg.text:
            cmd = int(msg.text.split(":")[1])
        task = asyncio.wait([self.clients[0].noop() for _ in range(cmd)])
        start = time.perf_counter()
        await task
        proc = time.perf_counter() - start
        result = f"トータル : {proc :3f}s\n" + \
                 f"平均 : {proc/cmd :3f}s"
        return await self.clients[0].sendMessage(msg.to, result)
    
    async def kickout_members(self, msg):
        """グループのメンバーを退会させます; キック:, kick:"""
        mids = await self.clients[0].getMidWithTag(msg)
        if not mids:
            cmd = msg.text.split(":")
            group = await self.clients[0].getGroup(msg.to)
            mids = list(filter(lambda c:cmd in c.displayName, group.members))
        task = [random.choice(self.clients[1:]).kickoutFromGroup(msg.to, mid) for mid in mids]
        return await asyncio.wait(task)
        
    async def send_call(self, msg):
        """連呼します;call, 連呼"""
        task = [self.clients[n].sendMessage(msg.to, f"[{n}] ok") for n in range(self.bot_length-1)]
        return await asyncio.wait(task)

    async def check_limit(self, msg):
        """規制確認をします;limit, 規制確認"""
        def is_limit(i):
            try:
                self.clients[i].run(self.clients[i].kickoutFromGroup(msg.to, self.bot_mids[i]))
                return False
            except:
                return True
        result = [f"{n} Limit {is_limit(n)}" for n in range(self.bot_length-1)]
        return await self.clients[0].sendMessage(msg.to, "\n".join(result))

    async def set_prefix(self, msg):
        """prefixを設定します;prefix:, 接頭辞:"""
        cmd = ":".join(msg.text.split(":")[1:])
        if cmd in self.user_data["prefix"]:
            return await self.clients[0].sendMessage(msg.to, f"[{cmd}] はすでに登録されています")
        self.user_data["prefix"].append(cmd)
        self.data_hander.write(self.user_data)
        return await self.clients[0].sendMessage(msg.to, "ok")

    async def send_setting(self, msg):
        """設定状況を確認します;setting, 設定"""
        result = "USJ仮保護bot\n" + \
                 "==保護状態==\n" + \
                f"蹴り保護 : {msg.to in self.user_data['group']['kick']}\n" + \
                f"参加保護 : {msg.to in self.user_data['group']['join']}\n" + \
                f"招待保護 : {msg.to in self.user_data['group']['invite']}\n" + \
                f"URL保護 : {msg.to in self.user_data['group']['url']}\n" + \
                "==その他==\n" + \
                f"接頭辞 : {self.user_data['prefix']}"
        return await self.clients[0].sendMessage(msg.to, result)

    async def join_kickers(self, msg):
        """キッカーを参加させます;join, 参加"""
        group :Group = await self.clients[0].getGroup(msg.to)
        if group.preventedJoinByTicket:
            group.preventedJoinByTicket = False
            group.name = group.name + "\n"
            await self.clients[0].updateGroup(group)
        ticket = await self.clients[0].reissueGroupTicket(msg.to)
        task = [self.clients[n].acceptGroupInvitationByTicket(msg.to, ticket) for n in range(self.bot_length-1)]
        await asyncio.wait(task)
        return await self.clients[0].sendMessage(msg.to, "ok")

    async def leave_group(self, msg):
        """グループを退会します;leave, 退会"""
        task = [self.clients[n].leaveGroup(msg.to) for n in range(self.bot_length-1)]
        return await asyncio.wait(task)

    async def __set_user_status_setting(self, msg, obj, mode):
        mids = await self.clients[0].getMidWithTag(msg)
        if not mids:
            mids = [s.strip() for s in msg.text.split(":")[2].split(",")]
        for mid in mids:
            await self.clients[0].getContact(mid)
            if mode == "add":
                if not mid in self.user_data["user"][obj]:
                    self.user_data["user"][obj].append(mid)
            elif mode == "del":
                if mid in self.user_data["user"][obj]:
                    self.user_data["user"][obj].remove(mid)
        await self.clients[0].sendMessage(msg.to, "\n".join(mids))
        self.data_hander.write(self.user_data)
        if mode == "add":
            return await self.clients[0].sendMessage(msg.to, f"上記{len(mids)}名を{obj}に追加しました")
        elif mode == "del":
            return await self.clients[0].sendMessage(msg.to, f"上記{len(mids)}名を{obj}から削除しました")

    async def set_user_status_with_black(self, msg):
        """ブラリスを設定します(black:mode: @mention or mids);black:, ブラリス:"""
        cmd = msg.text.split(":")[1]
        return await self.__set_user_status_setting(msg, "black", cmd)

    async def set_user_status_with_white(self, msg):
        """ホワリスを設定します(white:mode: @mention or mids);white:, ホワリス:"""
        cmd = msg.text.split(":")[1]
        return await self.__set_user_status_setting(msg, "white", cmd)

    async def set_user_status_with_admin(self, msg):
        """管理者を設定します(admin:mode: @mention or mids);admin:, 管理者:"""
        cmd = msg.text.split(":")[1]
        return await self.__set_user_status_setting(msg, "admin", cmd)
    
    async def reset_temp_black_list(self, msg):
        """一時ブラックリストの初期化をします;reset, 初期化"""
        self.temp_black.clear()
        return await self.clients[0].sendMessage(msg.ot, "ok")

    async def send_user_status(self, msg):
        """ユーザの状態を出します;user:, 状態:"""
        mids = await self.clients[0].getMidWithTag(msg)
        if not mids:
            mids = [s.strip() for s in msg.text.split(":")[1].split(",")]
        for mid in mids:
            await self.clients[0].getContact(mid)
            result = f"{mid}の状態\n" + \
                    f"ブラックリスト : {mid in self.user_data['user']['black']}\n" + \
                    f"ホワイトリスト : {mid in self.user_data['user']['white']}\n" + \
                    f"管理者リスト : {mid in self.user_data['user']['admin']}\n" + \
                    f"一時的ブラックリスト : {mid in self.temp_black}"
            await self.clients[0].sendMessage(msg.to, result)
        return True

    async def __set_protect_setting(self, msg, obj):
        cmd = msg.text.split(":")[1]
        is_protected = self.is_protected(msg, obj)
        if cmd == "on":
            if is_protected:
                return await self.clients[0].sendMessage(msg.to, f"[protect] {obj} はすでに{cmd} です")
            self.user_data["group"][obj].append(msg.to)
        elif cmd == "off":
            if not is_protected:
                return await self.clients[0].sendMessage(msg.to, f"[protect] {obj} はすでに{cmd} です")
            self.user_data["group"][obj].remove(msg.to)
        else:
            return

        self.data_hander.write(self.user_data)
        return await self.clients[0].sendMessage(msg.to , f"[protect] {obj}を{cmd}にしました")
    
    async def set_group_setting_with_kick_protect(self, msg):
        """蹴り保護を設定します;kick:, 蹴り保護:"""
        return await self.__set_protect_setting(msg, "kick")

    async def set_group_setting_with_join_protect(self, msg):
        """参加保護を設定します;join:, 参加保護:"""
        return await self.__set_protect_setting(msg, "join")

    async def set_group_setting_with_invite_protect(self, msg):
        """招待保護を設定します;invite:, 招待保護:"""
        return await self.__set_protect_setting(msg, "invite")

    async def set_group_setting_with_url_protect(self, msg):
        """URL保護を設定します;url:, URL保護:"""
        return await self.__set_protect_setting(msg, "url")

    async def set_group_setting_with_all_protect(self, msg):
        """全保護を設定します;all:, 全保護:"""
        task = asyncio.gather(
            self.__set_protect_setting(msg, "kick"),
            self.__set_protect_setting(msg, "join"),
            self.__set_protect_setting(msg, "invite"),
            self.__set_protect_setting(msg, "url")
        )
        return await task

    async def reboot_system(self, msg):
        """再起動します;reboot, 再起動"""
        await self.clients[0].sendMessage(msg.to, "wait")
        sys.argv.insert(0, "python3")
        return os.execvp("python3", sys.argv)

