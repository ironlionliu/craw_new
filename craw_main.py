# coding=utf-8
import threading, time, requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning) # 禁用安全请求警告
from pymongo import MongoClient
from json import *


from dbOperation import dbOperation
from stableIP import StableIP


#
def fetchUrl(db, step):
	trainNums = list(db["trainnum"].find({"status":"no"}).limit(step))
	return trainNums

def craw_one(db, proxy, query):
	commonUrl = "https://train.qunar.com/dict/open/seatDetail.do"
	url_paramSignal = "?"
	url_from = "dptStation=" + query["from"] + "&"
	url_to = "arrStation=" + query["to"] + "&"
	url_date = "date=" + "2017-11-11" + "&"
	url_num = "trainNo=" + query["trainnum"]
	url_rest = "&user=neibu&source=www&needTimeDetail=true"
	url = commonUrl + url_paramSignal + url_from + url_to + url_date + url_num + url_rest
	craw_result = requests.get(url,proxies=proxy,verify=False)
	if craw_result.status_code==200:
		craw_result = JSONDecoder().decode(str(craw_result.text))#也许已经是json格式了
		try:
			print(craw_result["data"]["trainNo"])
			db["trainnum"].update({"_id":query["_id"]},{"$set":{"status":"hasdata"}},upsert=False,multi=False)
			return craw_result
		except Exception as e:
			print(craw_result)


def craw(db, dbo, proxy, step, trainNumInfos):
	print("线程:" + threading.currentThread().getName() + "开启啦")
	craw_result = []
	for i in range(0,len(trainNumInfos)):
		oneResult = craw_one(db, proxy, trainNumInfos[i])
		try:
			print(oneResult["data"]["trainNo"])
			craw_result.append(oneResult)
		except Exception as e:
			pass
	trainNumInfo2Mongo(dbo,craw_result)

def multiCraws(db,dbo,eachStep):
	# eachStep = 20
	stableip = StableIP()
	proxies = stableip.getIPs("ip1.py")

	trainNumInfos = fetchUrl(db,eachStep*len(proxies))
	for i in range(0, len(proxies)):
		onethread = threading.Thread(target = craw,args=([db, dbo, proxies[i], eachStep, trainNumInfos[i*eachStep:(i+1)*eachStep]]), name = "name:"+str(i))
		onethread.start()



def initMongo():
	client = MongoClient()
	db = client.traincraw
	return db

def trainNum2Mongo(dbo,trainNumData,trainFrom,trainTo):
	table = "trainnum"
	tempData = []
	for i in range(0, len(trainNumData)):
		oneData = {"trainnum":trainNumData[i],"from":trainFrom[i],"to":trainTo[i],"status":"no"}
		tempData.append(oneData)
	trainNumData = tempData
	dbo.data2Mongo(table,trainNumData)

def trainNumInfo2Mongo(dbo,trainNumInfoData):
	table = "trainnuminfo"
	tempData = []
	for i in range(0, len(trainNumInfoData)):
		thisTrain = trainNumInfoData[i]
		oneData = {"trainnum":thisTrain["data"]["trainNo"],"stationItemList":[]}
		oneData["stationItemList"] = thisTrain["data"]["stationItemList"]
		# for j in range(0, len(trainNumInfoData[i]["stationItemList"])):
		# 	oneData["stationItemList"].append(thisTrain["stationItemList"][i]) 
		tempData.append(oneData)
	trainNumInfoData = tempData
	dbo.data2Mongo(table,trainNumInfoData)




def main():
	db = initMongo()
	dbo = dbOperation(db)


	# 初始化数据库
	trainNumData = dbo.readTrainFile("trainnum.txt")
	trainFrom = dbo.readTrainFile("from.txt")
	trainTo = dbo.readTrainFile("to.txt")
	# 将全部车次信息写入时开启
	# trainNum2Mongo(dbo,trainNumData,trainFrom,trainTo)
	


	# 每次爬取的数据为eachStep*ip个数，ip个数取决于ip1.py，也就是线程数
	eachStep = 40
	# 单线程爬虫并将爬取结果写入数据库测试，平时不要开启
	# trainNums = fetchUrl(db, eachStep) 
	# trainNumInfos = fetchUrl(db, eachStep)
	# trainnuminfo = craw(db, dbo, eachStep, trainNums)
	

	#多线程爬虫，第一次写数据库的时候不要开启
	multiCraws(db, dbo, eachStep)
	
	
	
	


# https://train.qunar.com/dict/open/seatDetail.do?dptStation=%E5%8C%97%E4%BA%AC%E5%8D%97&arrStation=%E4%B8%8A%E6%B5%B7%E8%99%B9%E6%A1%A5&date=2017-11-11&trainNo=G147&user=neibu&source=www&needTimeDetail=true

if __name__ == '__main__':
	main()


