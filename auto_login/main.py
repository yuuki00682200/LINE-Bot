from .run import Run
from api import Trace
import json

class LoginBot(Run):
    def __init__(self, client):
        self.client = client
        self.profile = self.client.run(self.client.getProfile())
        print(self.profile)
        self.mails  = "data/mails.json"
        self.trace  = Trace(self.client, False)
        Run.__init__(self)


    def main(self):
        self.trace.start(self.run, 100)

