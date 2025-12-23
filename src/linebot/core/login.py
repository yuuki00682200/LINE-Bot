from linebot.generated.line_api.TalkService import TalkService
from linebot.generated.line_api.AuthService import AuthService
from linebot.generated.line_api.AuthService.ttypes import LoginRequest, IdentityProvider, LoginResultType 
from linebot.generated.line_api.SecondaryLoginService import SecondaryLoginService, ttypes
from linebot.generated.f_line_api.TalkService import f_TalkService
from .get_client import Client
from .callback import Callback
from .config import Config
import requests
import asyncio
import sys
import rsa
import os


class Login(Config):
    certificate = ''

    def __init__(
            self,
            app_name=None,
            system_name=None,
            user_agent=None,
            callback=print,
            callback2=print,
            cert=None,
            connector=None):
        Config.__init__(self)
        if app_name:
            self.line_app = app_name
        if system_name:
            self.system_name = system_name
        if user_agent:
            self.user_agent = user_agent
        self.callback = Callback(callback, callback2)
        self.connector = connector
        self.cert = cert

    def login_with_auth_token(self, token):
        self.t_con._headers.update({"X-Line-Access": token})
        self.poll = self.t_con.get_client("/P4", f_TalkService)
        return self.t_con.get_client(self.talk_service, f_TalkService)

    def login_with_cert(self, _id, passwd, certificate=None, secondry=False):
        if self.mail_regex.match(_id):
            self.provider = IdentityProvider.LINE

        else:
            self.provider = IdentityProvider.NAVER_KR

        headers = {
            "X-Line-Application": self.line_app,
            "User-Agent": self.user_agent
        }
        if secondry:
            headers = {
                "User-Agent": self.user_agent_sec,
                "X-Line-Application": self.line_app_sec
            }
        self.t_con = Client(self.host, self.context, headers, self.connector)
        talk = self.t_con.get_client_with_sync(
            self.talk_service, TalkService)
        rsaKey = talk.getRSAKeyInfo(self.provider)
        message = (chr(len(rsaKey.sessionKey)) + rsaKey.sessionKey +
                   chr(len(_id)) + _id + chr(len(passwd)) + passwd).encode('utf-8')
        print(message)
        pub_key = rsa.PublicKey(int(rsaKey.nvalue, 16),
                                int(rsaKey.evalue, 16))
        crypto = rsa.encrypt(message, pub_key).hex()
        try:
            with open('certs/' + _id + '.crt', 'r') as f:
                self.certificate = f.read()
        except:
            if certificate:
                self.certificate = certificate
                if os.path.exists(certificate):
                    with open(certificate, 'r') as f:
                        self.certificate = f.read()

        auth_service = Client(self.host, self.context, headers, self.connector)
        auth = auth_service.get_client_with_sync(
            self.auth_service, AuthService)
        req = LoginRequest(
            type=0,
            identityProvider=self.provider,
            identifier=rsaKey.keynm,
            password=crypto,
            keepLoggedIn=True,
            accessLocation='8.8.8.8',
            systemName=self.system_name,
            certificate=self.certificate,
            e2eeVersion=0
        )
        result = auth.loginZ(req)
        if result.type == LoginResultType.REQUIRE_DEVICE_CONFIRM:
            self.callback.output(result.pinCode)
            headers = {
                "User-Agent": self.user_agent,
                "X-Line-Application": self.line_app,
                "X-Line-Access": result.verifier
            }
            if secondry:
                headers = {
                    "User-Agent": self.user_agent_sec,
                    "X-Line-Application": self.line_app_sec,
                    "X-Line-Access": result.verifier
                }
            access_key = requests.get(self.host + self.access_key, headers=headers)
            req = LoginRequest(
                type=1,
                keepLoggedIn=True,
                verifier=result.verifier,
                e2eeVersion=0)
            result = auth.loginZ(req)
        if result.type == LoginResultType.SUCCESS:
            if result.certificate:
                with open('certs/' + _id + '.crt', 'w') as f:
                    f.write(result.certificate)
                self.certificate = result.certificate
            if result.authToken:
                res = self.login_with_auth_token(result.authToken)
        elif result.type == LoginResultType.REQUIRE_QRCODE:
            res = self.login_with_qrcode()
        return res

    def login_with_qrcode(self, set_id=""):
        headers = {
            'User-Agent': self.user_agent_sec,
            'X-Line-Application': self.line_app_sec
        }
        self.t_con = Client(self.host, self.context, headers, self.connector)
        self.lgn = self.t_con.get_client_with_sync(self.login, SecondaryLoginService)
        self.get_qr_code()
        self.wait_url()
        if not self.varify_cert(set_id):
            self.get_pin()
            self.wait_pin()
        res = self.lgn.qrCodeLogin(
                ttypes.QrCodeLoginRequest(self.auth_session_id, self.system_name, True))
        if not os.path.isfile(f"certs/{self.cert}.session"):
            with open(f"certs/{self.cert}.session", "w") as f:
                f.write(res.certificate)
        return self.login_with_auth_token(res.accessToken)

    def get_qr_code(self):
        self.auth_session_id = self.lgn.createSession(ttypes.CreateQrSessionRequest()).authSessionId
        url = self.lgn.createQrCode(ttypes.CreateQrCodeRequest(self.auth_session_id))
        self.callback.output(url.callbackUrl)

    def wait_url(self):
        self.t_con.update_header({"X-Line-Access": self.auth_session_id})
        self.check_service = self.t_con.get_client_with_sync(self.check, SecondaryLoginService)
        self.check_service.checkQrCodeVerified(ttypes.CheckQrCodeVerifiedRequest(self.auth_session_id))
        self.t_con._headers.pop("X-Line-Access")
        
    def varify_cert(self, cert):
        try:
            self.lgn.verifyCertificate(ttypes.VerifyCertificateRequest(self.auth_session_id, cert))
            return True
        except:
            pass
        return False

    def get_pin(self):
        pin_code = self.lgn.createPinCode(ttypes.CreatePinCodeRequest(self.auth_session_id))
        self.callback.output_pin(pin_code.pinCode)

    def wait_pin(self):
        self.t_con.update_header({"X-Line-Access": self.auth_session_id})
        self.check_service.checkPinCodeVerified(ttypes.CheckQrCodeVerifiedRequest(self.auth_session_id))
        self.t_con._headers.pop("X-Line-Access")

