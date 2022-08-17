from .handler.data_handler import DataHandler
from api import LineClient
from aiohttp import ClientSession

class Login:
    def __init__(self):
        self.__connector = ClientSession()
        self.__result = []
        self.__mids   = []
        self.__login()

    def __login(self):
        data = DataHandler("address.json")
        for k, v in data.read().items():
            try:
                client = LineClient(k, v, connector=self.__connector)
                self.__result.append(client)
                profile = client.run(client.getProfile())
                self.__mids.append(profile.mid)
            except Exception as e:
                print(e)

    def get_clients(self):
        return self.__result
    
    def get_mids(self):
        return self.__mids

