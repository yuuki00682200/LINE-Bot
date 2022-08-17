from .handler.data_handler import DataHandler
from .polling import Polling
from .login import Login

class Protect(Polling):
    def __init__(self):
        self.data_handler = DataHandler("data/pub_prtect.json")
        
        self.__login_instance = Login()
        self.clients = self.__login_instance.get_clients()
        self.mids    = self.__login_instance.get_mids()
        self.bot_lengh = len(self.clients) - 1
        self._mid_to_client = self.__get_mid_to_client_dict()
        self.__initAll()

    def __initAll(self):
        Polling.__init__(self)

    def __get_mid_to_client_dict(self):
        return {self.mids[n]: self.clients[n] for n in range(self.bot_lengh)}

    def start(self):
        self.poll()
