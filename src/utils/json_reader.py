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

	def writeData(self, newData):
		self.data['data'] = newData
		output = json.dumps(self.data, indent=4)
		with open('../data.json', 'w') as outfile:
			outfile.write(output)

	def getServerKey(self):
		return self.data['token']

	def getUrl(self):
		return self.data['url']

	def getPass(self):
		return self.data['pass']

	def getData(self):
		return self.data['data']
