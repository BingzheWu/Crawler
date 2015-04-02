#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
	这个代码，主要用于库和表之间的特定数据转移工作
'''

from common.station_db import QueryBySQL
from common.insert_db import InsertStationTest
from common.station_insert_db import InsertStation

str = "SELECT * FROM `station`"
infos = QueryBySQL(str)


for line in infos:
	try:
		to_insert = [(line['type'],line['name'][:-2],line['map'],line['line'].strip(),'NULL','NULL',line['country_en'],line['country_ch'],line['city_en'],line['city_ch'],line['cityid'],line['num'],line['station_id'],line['interval_time'],line['price'],line['currency'])]
#		InsertStation(to_insert)
	except Exception,ex:
		print Exception,":",ex
		print line
