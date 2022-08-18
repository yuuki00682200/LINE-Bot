from line_api.TalkService.ttypes import (
    Group,
    Contact,
    Message)
import subprocess
import asyncio
import urllib
import time
import api
import sys
import os

class Command:
    def __init__(self):
        self.client: api.LineClient

    async def is_test(self, msg):
        """動作確認"""
        await self.client.sendMessage(msg.to, "ok")

    async def is_noop(self, msg):
        """noopの速度を計算します"""
        task = asyncio.wait([self.client.noop() for _ in range(1000)])
        start = time.time()
        await task
        end = time.time() - start
        result = f"tot: {end: 3f}s\n" + \
                 f"avg: {end/1000: 3f}s"
        await self.client.sendMessage(msg.to, result)

    async def is_help(self, msg):
        """説明書を出します"""
        result = 'USJbot help\n\n\\\\(使用例), {注意}//\n\n'
        funcs = [f for f, c in Command.__dict__.items()]
        fnum = 0
        for func in funcs:
            if func.startswith('st') or func.startswith('is'):
                doc = getattr(Command, func).__doc__
                if doc:
                    name = func[3:]
                    result += f"{name} >> {doc}\n\n"
                    fnum += 1
        await self.client.sendMessage(msg.to, f"{result}\ncommands :{fnum}")
    async def is_speed(self, msg):
        """受信時間(？)と送信速度を出します"""
        rec = time.time() - msg.createdTime / 1000
        start = time.time()
        await self.client.sendMessage(msg.to, f"{rec :3f}s")
        end = time.time() - start
        await self.client.sendMessage(msg.to, f"{end :3f}s")

    async def is_qrlogin(self, msg):
        """キッカーをQRでログインさせます"""
        kicker = api.LineClient(callback=lambda url: self.client.run(
            self.client.sendMessage(msg.to, url)), connector=self.connector)
        pro = await kicker.getProfile()
        self.kicker.append(kicker)
        self.mids.append(pro.mid)
        await self.client.sendMessage(msg.to, "ok")

    async def st_delete(self, msg):
        """きっかーの削除(delete:mail)"""
        cmd = msg.text[7:]
        if cmd in self.data["kicker"]:
            self.data["kicker"].pop(cmd)
            self.save_data()
            await self.client.sendMessage(msg.to ,"ok")

    async def st_kicker(self, msg):
        """キッカーの登録(kicker:mail:passwd)"""
        cmd = msg.text.split(":")
        if [cmd[1], cmd[2]] in self.data["kicker"]:
            return await self.client.sendMessage(msg.to, "登録済です")
        else:
            if not os.path.isfile(f"cert/{cmd[1]}.crt"):
                kicker = api.LineClient(
                        token=cmd[1], 
                        passwd=cmd[2], 
                        callback=lambda url: self.client.run(self.client.sendMessage(msg.to, url)), 
                        connector=self.connector)
                self.data["kicker"].append((cmd[1], cmd[2]))
                self.save_data()
            else:
                self.data["kicker"].append((cmd[1], cmd[2]))
                self.save_data()
        await self.client.sendMessage(msg.to, "ok")

    async def is_kicker(self, msg):
        """キッカーのログインをします"""
        for m, p in self.data["kicker"]:
            try:
                kicker = api.LineClient(token=m, passwd=p, connector=self.connector, sec=True)
                pro = await kicker.getProfile()
                self.mids.append(pro.mid)
                self.kicker.append(kicker)
            except:
                pass
        await self.client.sendMessage(msg.to, "ok")

    async def st_gidurl(self, msg):
        """gidからURLを生成します"""
        gid = msg.text[7:]
        ticket = await self.client.reissueGroupTicket(gid)
        await self.client.sendMessage(msg.to, "line.me/R/ti/g/" + ticket)

    async def is_gid(self, msg):
        """グループのIDを出します"""
        await self.client.sendMessage(msg.to, msg.to)

    async def is_gname(self, msg):
        """グループの名前を出します"""
        group = await self.client.getGroup(msg.to)
        await self.client.sendMessage(msg.to, group.name)

    async def is_reissue(self, msg):
        """グループのURLを取得,更新します"""
        ticket = await self.client.reissueGroupTicket(msg.to)
        await self.client.sendMessage(msg.to, "line.me/R/ti/g/" + ticket)

    async def is_gticket(self, msg):
        """グループのURL状態を出します"""
        group = await self.client.getGroup(msg.to)
        result = "open" if not group.preventedJoinByTicket else "close"
        await self.client.sendMessage(msg.to, result)

    async def is_gopen(self, msg):
        """グループのURLを開きます"""
        group = await self.client.getGroup(msg.to)
        if group.preventedJoinByTicket:
            group.preventedJoinByTicket = False
            await self.client.updateGroup(group)
            await self.client.sendMessage(msg.to, "ok.")

    async def is_gclose(self, msg):
        """グループのURLを閉じます"""
        group = await self.client.getGroup(msg.to)
        if not group.preventedJoinByTicket:
            group.preventedJoinByTicket = True
            await self.client.updateGroup(group)
            await self.client.sendMessage(msg.to, "ok.")

    async def is_gpic(self, msg):
        """グループのアイコンを出します"""
        group = await self.client.getGroup(msg.to)
        result = 'https://obs-sg.line-apps.com' + group.picturePath
        await self.client.sendMessage(msg.to, result)

    async def is_gtime(self, msg):
        """グループの作成時間を出します"""
        group = await self.client.getGroup(msg.to)
        result = time.ctime(group.createdTime/1000)
        await self.client.sendMessage(msg.to, result)

    async def is_gcreator(self, msg):
        """グループの作者のmidを出します"""
        group = await self.client.getGroup(msg.to)
        await self.client.sendMessage(msg.to, group.creator)

    async def is_gmember(self, msg):
        """グループのメンバーを出します"""
        group = await self.client.getGroup(msg.to)
        result = "\n".join([f"{c.displayName}: {c.mid}" for c in group.members])
        await self.client.sendMessage(msg.to, result)

    async def is_ginvite(self, msg):
        """グループの招待メンバーを出します"""
        group = await self.client.getGroup(msg.to)
        result = "\n".join([f"{c.displayName}: {c.mid}" for c in group.invitee])
        await self.client.sendMessage(msg.to, result)

    async def st_mk(self, msg):
        """メンションした人を退会させます(mk: @mention)"""
        mids = await self.client.getMidWithTag(msg)
        task = [self.client.kickoutFromGroup(msg.to, mid) for mid in mids]
        await asyncio.wait(task)

    async def st_nk(self, msg):
        """指定した文字が”名前”に含まれている人を退会させます(nk:text)"""
        group = await self.client.getGroup(msg.to)
        cmd = msg.text[3:]
        mids = [c.mid for c in filter(lambda c:cmd in c.displayName, group.members)]
        task = [self.client.kickoutFromGroup(msg.to, mid) for mid in mids]
        await asyncio.wait(task)

    async def st_ok(self, msg):
        """指定した文字が”コテハン”に含まれている人を退会させます(ok:text)"""
        group = await self.client.getGroup(msg.to)
        cmd = msg.text[3:]
        mids = [c.mid for c in filter(lambda c:cmd in c.displayNameOverridden if c.displayNameOverridden is not None else False, group.members)]
        task = [self.client.kickoutFromGroup(msg.to, mid) for mid in mids]
        await asyncio.wait(task)

    async def st_lk(self, msg):
        """指定した数字が”名前”の文字数と一致してる人を退会させます(lk:int)"""
        group = await self.client.getGroup(msg.to)
        cmd = int(msg.text[3:])
        mids = [c.mid for c in filter(lambda c:len(c.displayName) == cmd, group.members)]
        task = [self.client.kickoutFromGroup(msg.to, mid) for mid in mids]
        await asyncio.wait(task)

    async def st_sk(self, msg):
        """指定した文字が”ステメ”に含まれている人を退会させます(sk:text)"""
        group = await self.client.getGroup(msg.to)
        cmd = msg.text[3:]
        mids = [c.mid for c in filter(lambda c:cmd in c.statusMessage, group.members)]
        task = [self.client.kickoutFromGroup(msg.to, mid) for mid in mids]
        await asyncio.wait(task)

    async def is_kickall(self, msg):
        """グループのメンバーを退会させます"""
        group = await self.client.getGroup(msg.to)
        mids = [c.mid for c in group.members]
        task = [self.client.kickoutFromGroup(msg.to, mid) for mid in mids]
        await asyncio.wait(task)

    async def is_limit(self, msg):
        """自身の規制を確認します"""
        try:
            await self.client.kickoutFromGroup(msg.to, msg._from)
            await self.client.sendMessage(msg.to, "no limit")
        except:
            await self.client.sendMessage(msg.to, "limit")

    async def is_time(self, msg):
        """現在の時間を出します"""
        now = time.ctime()
        st = await self.client.getServerTime()
        server = time.ctime(st/1000)
        result = f"Pc {now}\n" + \
                 f"Line {server}"
        await self.client.sendMessage(msg.to, result)

    async def is_pname(self, msg):
        """自分の名前を出します"""
        contact = await self.client.getContact(msg._from)
        await self.client.sendMessage(msg.to, contact.displayName)

    async def is_pmid(self, msg):
        """自分のmid出します"""
        await self.client.sendMessage(msg.to, msg._from)

    async def is_pstatus(self, msg):
        """自分のステメを出します"""
        contact = await self.client.getContact(msg._from)
        await self.client.sendMessage(msg.to, contact.statusMessage)

    async def is_ppic(self, msg):
        """自分のアイコンを出します"""
        contact = await self.client.getContact(msg._from)
        result = 'https://obs-sg.line-apps.com' + contact.picturePath
        await self.client.sendMessage(msg.to, result)

    async def is_pcontact(self, msg):
        """自分の連絡先を送信します"""
        await self.client.sendContact(msg.to, msg._from)

    async def st_mmid(self, msg):
        """メンションした相手のmidを出します(mmid:@mention)"""
        mids = await self.client.getMidWithTag(msg)
        await self.client.sendMessage(msg.to, "\n".join(mids))

    async def st_mpic(self, msg):
        """メンションした相手のアイコンを出します(mpic:@mention)"""
        mids = await self.client.getMidWithTag(msg)
        contacts = await self.client.getContacts(mids)
        result = []
        for contact in contacts:
            result.append('https://obs-sg.line-apps.com' + contact.picturePath)
        await self.client.sendMessage(msg.to, "\n".join(result))

    async def st_mname(self, msg):
        """メンションした相手の名前を出します(mname:@mention"""
        mids = await self.client.getMidWithTag(msg)
        contacts = await self.client.getContacts(mids)
        result = []
        for contact in contacts:
            result.append(contact.displayName)
        await self.client.sendMessage(msg.to, "\n".join(result))
    
    async def st_mstatus(self, msg):
        """メンションした相手のステメを出します(mstatus:@mention)"""
        mids = await self.client.getMidWithTag(msg)
        contacts = await self.client.getContacts(mids)
        result = []
        for contact in contacts:
            result.append(contact.statusMessage)
        await self.client.sendMessage(msg.to, f"\n{'='*7}\n".join(result))

    async def st_mcontact(self, msg):
        """メンションした相手の連絡先を送信します(mcontact:@mention)"""
        mids = await self.client.getMidWithTag(msg)
        task = [self.client.sendContact(msg.to, mid) for mid in mids]
        await asyncio.wait(task)

    async def st_midname(self, msg):
        """midの名前を出します(midname:mid)"""
        mid = msg.text[8:]
        contact = await self.client.getContact(mid)
        await self.client.sendMessage(msg.to, contact.displayName)

    async def st_midpic(self, msg):
        """midのアイコンを出します(midpic:mid)"""
        mid= msg.text[7:]
        contact = await self.client.getContact(mid)
        result = 'https://obs-sg.line-apps.com' + contact.picturePath
        await self.client.sendMessage(msg.to, result)
    
    async def st_midstatus(self, msg):
        """midのステメを出します(midstatus:mid)"""
        mid = msg.text[10:]
        contact = await self.client.getContact(mid)
        await self.client.sendMessage(msg.to, contact.statusMessage)

    async def st_midcontact(self, msg):
        """midの連絡先を出します(midcontact:mid)"""
        mid = msg.text[11:]
        await self.client.sendContact(msg.to, mid)

    async def st_macro(self, msg):
        """指定回数送信します(macro:int:text)"""
        cmd = msg.text.split(':')
        num = int(cmd[1])
        text = ':'.join(cmd[2:])
        task = [self.client.sendMessage(msg.to, text) for _ in range(num)]
        await asyncio.wait(task)

    async def st_broad(self, msg):
        """指定した文字を一斉送信します(broad:text)"""
        text = msg.text[6:]
        gids = await self.client.getGroupIdsJoined()
        task = [self.client.sendMessage(gid, text) for gid in gids]
        await asyncio.wait(task)

    async def st_rename(self, msg):
        """自分の名前を変えます(rename:text)"""
        cmd = msg.text[7:]
        pro = await self.client.getProfile()
        pro.displayName = cmd
        await self.client.updateProfile(pro)
        await self.client.sendMessage(msg.to, "ok")

    async def st_restu(self, msg):
        """自分のステメを変えます(restu:text)"""
        cmd = msg.text[6:]
        pro = await self.client.getProfile()
        pro.statusMessage = cmd
        await self.client.updateProfile(pro)
        await self.client.sendMessage(msg.to, "ok")

    async def st_image(self, msg):
        """画像検索します(image:text)"""
        cmd = msg.text[6:]
        _, result = self.web.get_image_with_google(cmd)
        await self.client.sendMessage(msg.to, result)
    
    async def st_lyric(self, msg):
        """曲名から歌詞を検索します(lyric:text)"""
        cmd = msg.text[6:]
        result, _, _, _ = self.web.get_lyric(cmd)
        await self.client.sendMessage(msg.to, result)

    async def st_ymusic(self, msg):
        """曲名からYouTubeURLを探します(ymusic:text)"""
        cmd = msg.text[7:]
        _, result, _, _ = self.web.get_lyric(cmd)
        await self.client.sendMessage(msg.to, result)

    async def st_surl(self, msg):
        """URLを短縮します(surl:text)"""
        cmd = msg.text[5:]
        result = self.web.get_short_url(cmd)
        await self.client.sendMessage(msg.to, result)

    async def st_weather(self, msg):
        """天気を出します(weather:text)"""
        cmd = msg.text[8:]
        _, result = self.yahoo.get_weather(cmd)
        await self.client.sendMessage(msg.to, '\n'.join([f"{t} : {w}" for t,w in result.items()]))

    async def st_wurl(self, msg):
        """天気情報のURLを出します(wurl:text)"""
        cmd = msg.text[5:]
        result = self.yahoo.get_url(cmd)
        await self.client.sendMessage(msg.to, result)

    async def st_google(self, msg):
        """Google検索したURLを出します(google:text)"""
        cmd = msg.text[7:]
        url = 'http://www.google.co.jp/search?jl=ja&num=100&q='
        encoded = urllib.parse.quote(cmd)
        await self.client.sendMessage(msg.to, url+encoded)

    async def st_youtube(self, msg):
        """YouTubeで検索したURLを出します(youtube:text)"""
        cmd = msg.text[8:]
        url = 'https://www.youtube.com/results?search_query='
        encoded = urllib.parse.quote(cmd)
        await self.client.sendMessage(msg.to, url+encoded)

    async def st_xvideos(self, msg):
        """Xvideosで検索したURLを出します(xvideos:text)"""
        cmd = msg.text[8:]
        url = "https://www.xvideos.com/?k="
        encoded = urllib.parse.quote(cmd)
        await self.client.sendMessage(msg.to, url+encoded)
    async def is_leave(self, msg):
        """グループを退会します"""
        await self.client.sendMessage(msg.to, "USJbotはいいゾ")
        await self.client.leaveGroup(msg.to)

    async def is_grouplist(self, msg):
        """参加してるグループのidを出します"""
        gids = await self.client.getGroupIdsJoined()
        await self.client.sendMessage(msg.to, '\n'.join(gids))

    async def is_groupnamelist(self, msg):
        """参加しているグループのidと名前を出します"""
        gids = await self.client.getGroupIdsJoined()
        groups = await self.client.getGroups(gids)
        name_and_id = [f"{g.name} > {g.id}" for g in groups]
        await self.client.sendMessage(msg.to, "\n".join(name_and_id))

    async def st_midin(self, msg):
        """midを招待します(midin:mid)"""
        mid = msg.text[6:]
        await self.client.inviteIntoGroup(msg.to, [mid])

    async def st_nin(self, msg):
        """指定した文字が”なまえ”に含まれている人を招待します(nin:text)"""
        cmd = msg.text[4:]
        mids = await self.client.getAllContactIds()
        contacts = await self.client.getContacts(mids)
        mids = [c.mid for c in filter(lambda c:cmd in c.displayName, contacts)]
        await self.client.inviteIntoGroup(msg.to, mids)

    async def st_midcan(self, msg):
        """midをキャンセルします(midcan:mid)"""
        mid = msg.text[7:]
        await self.client.cancelGroupInvitation(msg.to, mid)

    async def st_ncan(self, msg):
        """指定した文字が”なまえ”に含まれている人をキャンセルします{量が多いと一時凍結します}(ncan:text)"""
        cmd = msg.text[5:]
        group = await self.client.getGroup(msg.to)
        mids = [c.mid for c in group.invitee]
        contacts = await self.client.getContacts(mids)
        mids = [c.mid for c in filter(lambda c:cmd in c.displayName, contacts)]
        task = [self.client.cancelGroupInvitation(msg.to, mid) for mid in mids]
        await asyncio.wait(task)

    async def is_memberadd(self, msg):
        """グループのメンバーを追加します{150人以上は三秒感覚で追加します}"""
        group = await self.client.getGroup(msg.to)
        member = group.members
        if len(member) > 150:
            mids = [c.mid for c in member]
            task = [lambda mid:(self.client.findAndAddContactsByMid(mid), time.sleep(3)) for mid in mids]
            await asyncio.wait(task)
        else:
            mids = [c.mid for c in member]
            task = [self.client.findAndAddContactsByMid(mid) for mid in mids]
            await asyncio.wait(task)
        await self.client.sendMessage(msg.to, "ok.")

    async def st_nadd(self, msg):
        """指定した文字が”名前”に含まれている人を追加します(nadd:text)"""
        group = await self.client.getGroup(msg.to)
        cmd = msg.text[5:]
        mids = [c.mid for c in filter(lambda c:cmd in c.displayName, group.members)]
        task = [self.client.findAndAddContactsByMid(mid) for mid in mids]
        await asyncio.wait(task)
        await self.client.sendMessage(msg.to, "ok.")
        
    
    async def st_madd(self, msg):
        """メンションした相手を追加します(madd:@mention)"""
        mids = await self.client.getMidWithTag(msg)
        task = [self.client.findAndAddContactsByMid(mid) for mid in mids]
        await asyncio.wait(task)
        await self.client.sendMessage(msg.to, "ok.")

    async def st_all_gr(self, msg):
        """全グループ参加挨拶を切り替えます(all_gr:on/off)"""
        cmd = msg.text[7:]
        mode = cmd == "on"
        self.data["auto"]["greeting"] = mode
        self.save_data()
        await self.client.sendMessage(msg.to, "ok")

    async def st_all_read(self, msg):
        """全グループ自動既読を切り替えます(all_read:on/off)"""
        cmd = msg.text[9:]
        mode = cmd == "on"
        self.data["auto"]["read"] = mode
        self.save_data()
        await self.client.sendMessage(msg.to, "ok")

    async def st_all_restore(self, msg):
        """全グループ取り消し復元を切り替えます(all_restore:on/off)"""
        cmd = msg.text[12:]
        mode = cmd == "on"
        self.data["auto"]["restore"] = mode
        self.save_data()
        await self.client.sendMessage(msg.to, "ok")

    async def st_join(self, msg):
        """自動参加を切り替えます(join:on/off)"""
        cmd = msg.text[5:]
        mode = cmd == "on"
        self.data["auto"]["join"] = mode
        self.save_data()
        await self.client.sendMessage(msg.to, "ok")

    async def st_leave(self, msg):
        """自動退出を切り替えます(leave:on/off)"""
        cmd = msg.text[6:]
        mode = cmd == "on"
        self.data["auto"]["leave"] = mode
        self.save_data()
        await self.client.sendMessage(msg.to, "ok")

    async def st_add(self, msg):
        """自動追加返しを切り替えます(add:on/off)"""
        cmd = msg.text[4:]
        mode = cmd == "on"
        self.data["auto"]["add"] = mode
        self.save_data()
        await self.client.sendMessage(msg.to, "ok")

    async def st_read(self, msg):
        """自動既読を切り替えます(read:on/off)"""
        cmd = msg.text[5:]
        if cmd == "on":
            self.data["group"]["read"].append(msg.to)
        else:
            self.data["group"]["read"].remove(msg.to)
        self.save_data()
        await self.client.sendMessage(msg.to, "ok")

    async def st_restore(self, msg):
        """取り消し復元を切り替えます(restore:on/off)"""
        cmd = msg.text[8:]
        if cmd == "on":
            self.data["group"]["restore"].append(msg.to)
        else:
            self.data["group"]["restore"].remove(msg.to)
        self.save_data()
        await self.client.sendMessage(msg.to, "ok")

    async def st_gre(self, msg):
        """参加挨拶を切り替えます(gre:on/off)"""
        cmd = msg.text[4:]
        if cmd == "on":
            self.data["group"]["greeting"].append(msg.to)
        else:
            self.data["group"]["greeting"].remove(msg.to)
        self.save_data()
        await self.client.sendMessage(msg.to, "ok")
    
    async def st_greeting(self, msg):
        """参加挨拶のあれを変更します(greeting:text)"""
        cmd = msg.text[9:]
        self.data["text"]["greeting"] = cmd
        self.save_data()
        await self.client.sendMessage(msg.to, "ok")
        
    async def st_gs(self, msg):
        """グループのメンバーに一斉送信します(gs:text)"""
        cmd = msg.text[3:]
        group = await self.client.getGroup(msg.to)
        mids = [c.mid for c in group.members]
        task = [self.client.sendMessage(mid, cmd) for mid in mids]
        await asyncio.wait(task)
        await self.client.sendMessage(msg.to, "ok")

    async def st_kickba(self, msg):
        """蹴り返し(kickba:on/off)"""
        cmd = msg.text[7:]
        if cmd == "on":
            self.data["group"]["kick"].append(msg.to)
        elif cmd == "off":
            self.data["group"]["kick"].delete(msg.to)
        self.save_data()
        await self.client.sendMessage(msg.to, "ok")

    async def st_rk(self, msg):
        """指定した人数蹴ります(rk:int)"""
        cmd = int(msg.text[3:])
        group = await self.client.getGroup(msg.to)
        mids = [con.mid for con in group.members]
        task = [self.client.kickoutFromGroup(msg.to, mid) for mid in mids[:cmd]]
        await asyncio.wait(task)

    async def is_sekick(self, msg):
        """瀬が名前の最後に含まれる人をけります"""
        group = await self.client.getGroup(msg.to)
        mids = [con.mid for con in filter(lambda x:"瀬" in x.displayName, group.members)]
        task = [self.client.kickoutFromGroup(msg.to, mid) for mid in mids]
        await asyncio.wait(task)

    async def st_group(self, msg):
        """メンションした人を新グループに招きます(group:@mention)"""
        mids = await self.client.getMidWithTag(msg)
        await self.client.createGroup("USJbotはいいゾ", mids)
        await self.client.sendMessage(msg.to, "ok")
    
    async def st_error(self, msg):
        """エラーを出します(error:index)"""
        cmd = int(msg.text[6:])
        err = self.trace.error[cmd]
        await self.client.sendMessage(msg.to, str(err))

    async def st_addid(self, msg):
        cmd = msg.text[6:]
        con = await self.client.findContactByUserid(cmd)
        print(con)
        await self.client.sendContact(msg.to, con.mid)

    async def is_fgopen(self, msg):
        """無理やりやります"""
        group : Group= await self.client.getGroup(msg.to)
        _name = group.name
        group.name = _name + "\n"
        group.preventedJoinByTicket = False
        group.pictureStatus = group.picturePath + "/a"
        await self.client.updateGroup(group)
        await self.client.sendMessage(msg.to, "ok")

    async def st_select(self, msg):
        """選択します(select:@mention)"""
        mids = await self.client.getMidWithTag(msg)
        self.selects += mids
        await self.client.sendMessage(msg.to, "ok")

    async def is_kick(self, msg):
        """選択した人たちを蹴ります"""
        task = [self.client.kickoutFromGroup(msg.to, mid) for mid in self.selects]
        await asyncio.wait(task)
        self.selects.clear()

    async def is_selected(self, msg):
        """選択した人たち"""
        contacts = await self.client.getContacts(self.selects)
        names = [con.displayName for con in contacts]
        await self.client.sendMessage(msg.to, "\n".join(names))

    async def is_invite(self, msg):
        """選択した人たちを招く"""
        await self.client.inviteIntoGroup(msg.to, self.selects)
        await self.is_clear(msg)

    async def is_clear(self, msg):
        """選択したやつの初期化"""
        self.selects.clear()
        await self.client.sendMessage(msg.to, "ok")

    async def st_takeover(self, msg):
        """データを引き継ぎます(takeover:@mention)"""
        mids = await self.client.getMidWithTag(msg)
        if os.path.isfile(f"data/data_{mids[0]}.json"):
            return
        with open(f"data/data_{mids[0]}.json", "w") as f:
            f.write(str(self.data))
        await self.client.sendMessage(msg.to, "ok")

    async def is_protect(self, msg):
        """保護起動"""
        subprocess.Popen(["python3", "protect.py", self.mids[0]])
        await self.client.sendMessage(msg.to, "ok")

    async def is_setting(self, msg):
        """設定確認"""
        auto = self.data["auto"]
        group = self.data["group"]
        result = "全グループのやつ\n\n" + \
                 f"強制抜けるやつ {auto['leave']}\n" + \
                 f"既読つける {auto['read']}\n" + \
                 f"ついか {auto['add']}\n" + \
                 f"ふくげん {auto['restore']}\n" + \
                 f"あいさつ {auto['greeting']}\n" + \
                 "グループべつ系男子\n\n" + \
                 f"きどく {msg.to in group['read']}\n" + \
                 f"けりかえし {msg.to in group['kick']}\n" + \
                 f"ふくげん {msg.to in group['restore']}\n" + \
                 f"あいさつ {msg.to in group['greeting']}\n\n" + \
                 f"設定中のあいさつ {self.data['text']['greeting']}\n" + \
                 f"登録済のキッカー {len(self.data['kicker'])}"
        await self.client.sendMessage(msg.to, result)

