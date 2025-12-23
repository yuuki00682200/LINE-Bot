from frugal.context import FContext
from .login import Login
from .talk import Talk
import nest_asyncio
import asyncio
import os


class LineClient(Login, Talk):
    def __init__(
            self,
            token=None,
            passwd=None,
            app_name=None,
            system_name=None,
            user_agent=None,
            callback=print,
            callback2=print,
            sec=False,
            connector=None,
            cert=None,
            loop=None):
        self.context = FContext()
        if loop is not None:
            self.loop = loop
        else:
            self.loop = asyncio.get_event_loop()
        Login.__init__(
            self,
            app_name,
            system_name,
            user_agent,
            callback=callback,
            callback2=callback2,
            cert=cert,
            connector=connector)
        if token and passwd:
            self.client = self.login_with_cert(token, passwd, secondry=sec)
        elif token is not None:
            self.client = self.login_with_auth_token(token)
        else:
            set_id = None
            if cert:
                if os.path.isfile(f"certs/{cert}.session"): 
                    with open(f"certs/{cert}.session", "r") as f:
                        set_id = f.read()
            self.client = self.login_with_qrcode(set_id)
        Talk.__init__(self)

    def run(self, coro):
        nest_asyncio.apply()
        return self.loop.run_until_complete(coro)
