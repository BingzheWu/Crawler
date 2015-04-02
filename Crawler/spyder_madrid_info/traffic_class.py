#!/usr/bin/env python
#-*- coding:utf-8 -*-

'''
	@author: chunzhi
	@date  : 2014-11-07
	@desc  : traffic class when process the traffic
	@aim   : beautiful and powerful code 
'''

import os
import copy
import time
import datetime
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import urllib2
import json

def countTime(timeA,timeB):
	n1 = int(timeA.split(':')[0])*60 + int(timeA.split(':')[1])
	n2 = int(timeB.split(':')[0])*60 + int(timeB.split(':')[1])
	return abs(n1-n2)

def process_time_dict(task_dict):
	res = ''
	week_list = ['mon','tue','wed','thu','fri']
	holiday_list = ['1.1','4.18','4.21','5.5','5.26','8.25','12.25','12.26']
	for key,value in task_dict.items():
		value1 = value.replace(':','.',10)
		if '-' in key or 'and' in key:
			if '-' in key:
				for i in week_list:
					res += ( '[' + i + ':' + value1 + ']' ) 
			if 'and' in key:
				res += ( '[' + 'sat' + ':' + value1 + ']' )
				for i in holiday_list:
					res += ( '[' + i + ':' + value1 + ']' )
		else:
			res += ( '[' +  key + ':' + value1 + ']')

	return res

class line:
	def __init__(self):
		self.line_id = ''
		self.line_name = ''
		self.line_intervalTime = ''
		self.line_tableTime = ''
		self.line_price = ''
		self.line_currency = ''
		self.line_mode = ''
	def set_data(self,line_id='NULL',line_name='NULL',line_intervalTime='NULL',\
			line_tableTime='NULL',line_price='NULL',line_currency='NULL',\
			line_mode='NULL'):
		self.line_id,self.line_name,self.line_intervalTime,self.line_tableTime,\
				self.line_price,self.line_currency,self.line_mode = \
				line_id, line_name, line_intervalTime, line_tableTime,\
				line_price,line_currency,line_mode
	def output(self):
		print ( 'line_name=%s,intervalTime=%s,tableTime=%s'%( \
				self.line_name,self.line_intervalTime,self.line_tableTime ) )

class route(line):
	def __init__(self,line):
		self.__dict__ = line.__dict__.copy()
		self.__route_name = 'NULL'
		self.__oriId   = 'NULL'
		self.__desId   = 'NULL'
		self.__stations = []
		self.__time = 'NULL'
	
	def append_station(self,sta):
		self.__stations.append(sta)
	def show_route_name(self):
		print self.__route_name
		return self.__route_name
	def show_stations(self):
		tmp_list = []
		for i in self.__stations:
			#print i.station_name
			tmp_list.append( i.output() )
		tmp_list = '&&&'.join(tmp_list)
		tmp_list += (self.__time)
		tmp_list = self.__route_name + '###NULL###NULL###NULL###' + tmp_list
		return tmp_list

	def show_station_name(self):
		tmp_list = []
		for i in self.__stations:
			tmp_list.append(i.station_name)
		return tmp_list

	def get_reverse_route(self):
		tmp_list = []
		t_stations = copy.copy(self.__stations)
		t_stations.reverse()
		t_cnt = 0 
		t_sum_run_time = t_stations[0].station_run_time
		for i in t_stations:
			t_cnt += 1
			i.station_run_time = abs( t_sum_run_time - i.station_run_time )
			i.station_num = t_cnt
			tmp_list.append( i.output() )
		tmp_list = '&&&'.join(tmp_list)
		tmp_list += (self.__time)
		tmp_list = self.__route_name + '_R###NULL###NULL###NULL###' + tmp_list
		return tmp_list

	def set_data(self,route_name='NULL',route_direction='NULL',oriId='NULL',desId='NULL'):
		self.__route_name = route_name
		self.__oriId = oriId
		self.__desId = desId
	def get_from_to_to(self):
		FROM = self.__stations[0].station_id
		TO   = self.__stations[-1].station_id
		return FROM,TO
	def numOfStations(self):
		return str(len(self.__stations))
	def showStations(self):
		tmp_list = []
		for i in self.__stations:
			tmp_list.append(i.station_id)
		tmp_list = '&'.join(tmp_list)
		return tmp_list

	def get_from(self):
		return self.__stations[0].station_id
	def get_station_id(self):
		tmp_list = []
		for i in self.__stations:
			tmp_list.append(i.station_id)
		return tmp_list
	def set_time(self,time = 'NULL'):
		self.__time = time
		return

	def set_running_time(self, runtime_dict):
		print runtime_dict
		for i in self.__stations:
			i.set_run_time( runtime_dict[ i.station_id ] )
		for i in self.__stations:
			print i.station_run_time
		return

class station:
	def __init__(self):
		self.station_id = ''
		self.map_info = ''
		self.station_name = ''
		self.station_num = ''
		self.station_run_time = 'NULL'
	
	def set_run_time(self,time):
		self.station_run_time = time
		return
		

	def output(self):
		#for name,value in vars(self).items():
		#	print( '%s = %s '% (name,value) )
		if self.station_run_time == 'NULL':
			self.station_run_time = ( self.station_num - 1 ) * 2
		return self.station_name+'&'+self.map_info+'&'+\
				str(self.station_num)+'&'+str(self.station_run_time)

