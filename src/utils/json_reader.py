import json

class JsonReader():

    def getServerKey(self):
        key = {}
        try:
            files = open("../data.json")
            key = json.load(files)
            files.close()
        except Exception as e:
            print("Couldn't load json")

        return key['token']
