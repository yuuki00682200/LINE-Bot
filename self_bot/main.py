from .web_data import WebData
from .yahoo import Yahoo
from .run import Run
import json
import api
import os

class Selfbot(Run):
    def __init__(self, client, connector, mid):
        self.client = client
        self.client.run(self.client.updateSettingsAttribute(0, 65536, "bF"))

        self.web = WebData()
        self.yahoo = Yahoo()
        self.connector = None
        self.kicker = []
        self.mids   = [mid]
        self.selects = []
        self.message = {}
        self.trace = api.Trace(self.client)
        self.data = self.read_data(self.mids[0])
        Run.__init__(self)

    def read_data(self, mid):
        data = f"data/data_{mid}.json"
        if os.path.isfile(data):
            with open(data, "r") as f:
                result = json.load(f)
        else:
            with open("temp.json", "r") as f:
                temp = json.load(f)
            with open(data, "w") as f:
                json.dump(temp, f)
            result = temp
        return result

    def save_data(self):
        data = f"data/data_{self.mids[0]}.json"
        with open(data, "w") as f:
            json.dump(self.data, f)
        return self.data

    def main(self):
        self.trace.start(self.run, 100)

