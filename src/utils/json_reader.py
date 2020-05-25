import json

class JsonReader():

	def __init__(self):
		self.data = {}
		try:
			files = open("../data.json")
			self.data = json.load(files)
			files.close()
		except Exception as e:
			print("Couldn't load json")
			print(e)

	def getServerKey(self):
		return self.data['token']

	def getUrl(self):
		return self.data['url']

	def getData(self):
		return self.data['data']
