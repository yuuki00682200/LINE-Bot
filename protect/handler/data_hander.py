import json
import os

class DataHandler:
    def __init__(self, fp):
        self.__fp = fp
        if not os.path.isfile(self.__fp):
            self.__create_data()

    def read(self):
        opener = open(self.__fp, "r")
        result = json.load(opener)
        opener.close()
        return result

    def write(self, obj):
        opener = open(self.__fp, "w")
        return json.dump(obj, opener, ensure_ascii=False)

    def __create_data(self):
        opener = open(self.__fp, "w")
        with open("protect_temp.json", "r") as f:
            obj = json.load(f)
            json.dump(obj, opener)
        return opener.close()

