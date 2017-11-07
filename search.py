# coding=utf-8
import threading, time, requests, re
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning) # 禁用安全请求警告
from pymongo import MongoClient
from json import *


from dbOperation import dbOperation



def initMongo():
	client = MongoClient()
	db = client.traincraw
	return db


def goThrough(db, dbo, data, city):
	result = []
	for i in range(0,len(data)):
		result.append(data[i]["stationItemList"])

	xCity = []
	for i in range(0,len(result)):
		for j in range(0,len(result[i])):
			if re.match(city, result[i][j]["stationName"], flags=0):
				xCity.append(result[i])
				break
	return xCity



def main():
	db = initMongo()
	dbo = dbOperation(db)
	data = dbo.findTrainNumInfo()
	cities = ["上海","北京","广州","深圳","天津","重庆","苏州","武汉","武昌","汉口","成都","杭州","南京","青岛","长沙","沧州","沈阳","漳州","盐城","石家庄","伊宁","洛阳"]
	for i in range(0,len(cities)):
		xCity = goThrough(db, dbo, data, cities[i])
		print("经过" + cities[i] + "的列车有：" + str(len(xCity)) + "趟")
	
	
	
	


# https://train.qunar.com/dict/open/seatDetail.do?dptStation=%E5%8C%97%E4%BA%AC%E5%8D%97&arrStation=%E4%B8%8A%E6%B5%B7%E8%99%B9%E6%A1%A5&date=2017-11-11&trainNo=G147&user=neibu&source=www&needTimeDetail=true

if __name__ == '__main__':
	main()
