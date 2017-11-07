from pymongo import MongoClient

class dbOperation():
	def __init__(self,db):
		self.name = "hello dbOperation"
		self.db = db
		pass

	
	def data2Mongo(self,table,data):
		print("data2Mongo")
		for i in range(0,len(data)):
			self.db[table].insert_one(data[i])
		pass


	def readTrainFile(self,fileName):
		data = open(fileName,'r')
		trainNumData = []
		while 1:
			line = data.readline()
			line = line.replace("\n","")
			if not line:
				break
			trainNumData.append(line)
		return trainNumData

	def findTrainNumInfo(self):
		data = list(self.db["trainnuminfo"].find())
		# data = list(self.db["trainnuminfo"].find({"text":{'$regex' : ".*atmosphere.*"}}))
		return data








version = "0.1"