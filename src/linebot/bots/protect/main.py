from .handler.data_handler import DataHandler
from .command_check import CommandCheck
from .runner import Runner
from .debug import Debug
from.login import Login
from linebot.core.trace import Trace

class Protect(Runner):
    def __init__(self, mid):
        self.data_hander = DataHandler(f"data/protect_{mid}.json")
        self.__invite_protect = {}
        self.temp_black  = []
        self.user_data   = self.data_hander.read()
        self.user_data["user"]["admin"].append(mid)

        self.__login_instance = Login(DataHandler(f"data/data_{mid}.json").read())
        self.clients = self.__login_instance.get()
        self.bot_mids = self.__login_instance.get_mids()
        self.bot_length = len(self.clients)
        self.tracer  = Trace(self.clients[0])

        self.errors  = self.tracer.error

        self.command_handler = CommandCheck(self.user_data["prefix"])
    
        self.debug   = Debug(debug=True)

        print("run")
        self.clients[0].run(self.clients[0].sendMessage(mid, "run!"))

    def __initAll(self):
        Runner.__init__(self)

    def start(self):
        self.tracer.start(self.run, 100)
    
