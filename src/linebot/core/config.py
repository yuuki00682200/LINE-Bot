import re

class Config:
    def __init__(self):
        self.host = 'https://gd2.line.naver.jp'
        self.auth_service = '/api/v4p/rs'
        self.talk_service = '/api/v4/TalkService.do'
        self.login = "/acct/lgn/sq/v1"
        self.check = "/acct/lp/lgn/sq/v1"
        self.access_key = '/Q'
        self.line_app = 'CHROMEOS\t2.3.3\tChrome_OS\t1'
        self.line_app_sec = "ANDROIDLITE\t2.11.1\tAndroid·OS\t10.1;SECONDARY"
        self.user_agent = 'Mozilla/5.0·(X11;·Linux·x86_64)·AppleWebKit/537.36·(KHTML,·like·Gecko)·Chrome/77.0.3865.120·Safari/537.36'
        self.user_agent_sec = "LLA/2.11.1·Nexus·5X·10"
        #self.line_app = 'IOSIPAD\t10.0.0\tiOS\t13.3'
        #self.user_agent = 'Line/10.0.0'
        self.system_name = 'USJ Bot'
        self.mail_regex = re.compile(r"[^@]+@[^@]+\.[^@]+")
