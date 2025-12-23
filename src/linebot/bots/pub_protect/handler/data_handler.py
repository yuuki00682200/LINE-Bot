import json
import os

class DataHandler:
    def __init__(self, fp):
        self.__fp = fp

    def read(self):
        with open(self.__fp, "r") as fp:
            return json.load(fp)

    def write(self, obj):
        with open(self.__fp, "w") as fp:
            return json.dump(obj, fp, ensure_ascii=False)

