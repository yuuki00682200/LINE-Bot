from linebot.generated.line_api.AuthService.ttypes import TalkException
from aiohttp import ClientSession
from linebot.core.client import LineClient

class Login:
    def __init__(self, addr):
        self.addr = addr
        self.__mids = []
        self.__connector = ClientSession()
        self.__result = self.__login()

    def __login(self):
        result = []
        for m, p in self.addr["kicker"]:
            try:
                kicker = LineClient(token=m, passwd=p, connector=self.__connector)
                result.append(kicker)
                self.__mids.append(kicker.run(kicker.getProfile()).mid)
            except TalkException as e:
                print(e, m)
            except BaseException as e:
                print(e)
        return result
    
    def get(self):
        return self.__result

    def get_mids(self):
        return self.__mids
