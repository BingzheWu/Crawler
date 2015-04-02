
#-*- coding:utf-8 -*-


import re
import copy
import Queue
import urllib2
from traffic_class import line,route
from traffic_class import station as STATION

class station:
	def __init__(self):
		self.type = 'Metro'
		self.name = ''
		self.map = ''
		self.line = ''
		self.country_en = 'SPN'
		self.country_ch = '西班牙'
		self.city_en = 'MAD'
		self.city_ch = '马德里'
		self.num = ''
		self.station_id = 'NULL'
		self.interval_time = 'NULL'
		self.price = 'NULL'
		self.currency = 'NULL'
		self.step = 1
		self.Referer = ''
		self.url = ''
	
	def output(self):
		print 'step='+str(self.step)
		print self.url
		print self.Referer
	def showStation(self):
		print 'self.type = %s, self.name = %s, self.map = %s, self.line = %s, self.country_en = %s,\
				self.country_ch = %s, self.city_en = %s, self.city_ch = %s, self.num = %s, self.station_id = %s,\
				self.interval_time = %s, self.price = %s, self.currency = %s '%(self.type,self.name,self.map,self.line,self.country_en,\
				self.country_ch,self.city_en,self.city_ch,self.num,self.station_id,\
				self.interval_time,self.price,self.currency )




def bfs(it):
	hd =  {
			'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:32.0) Gecko/20100101 Firefox/32.0    ',
			'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
			'Accept-Language':'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3',
			'Proxy-Connection':'keep-alive',
			}
	myqueue = Queue.Queue(maxsize = 0 )
	myqueue.put(it)
	station_list = []
	while myqueue.qsize() > 0:
		temp = myqueue.get()
		temp.output()
		print myqueue.qsize()
		hd_t = copy.copy(hd)
		hd_t['Referer'] = temp.Referer
		req = urllib2.Request(temp.url,headers=hd_t)
		content = urllib2.urlopen(req).read()
		host = 'http://www.metromadrid.es'
		if temp.step == 1:
			c1 = re.compile('([^"]+html)">View Stations([^<]+)')
			lines = c1.findall(content)
             for i in lines[:1]:
				tt = copy.copy(temp)
				tt.step = temp.step+1
				tt.url = host.strip()+i[0].strip()
				tt.Referer = temp.url
				tt.line = i[1].strip()
				myqueue.put(tt)
		elif temp.step == 2:
			c2 = re.compile('href="([^"]+html)">([^<]+)</a></td>')
			stations = c2.findall(content)
			cnt = 0
			for i in stations:
				cnt += 1
				tt = copy.copy(temp)
				tt.step = temp.step+1
				tt.num = cnt
				tt.url = host.strip() + i[0].strip()
				tt.Referer = temp.url
				tt.name = i[1].strip()
				myqueue.put(tt)
		elif temp.step == 3:
			turl = re.search('http://www.metromadrid.es/metro/metronet/mapa.aspx\?tipo=ESTACION&amp;idParada=\d+&amp;idioma=en',content).group()
			turl = turl.replace('amp;','',10)
			tt = copy.copy(temp)
			tt.step = temp.step+1
			tt.url = turl
			tt.Referer = temp.url
			myqueue.put(tt)
		elif temp.step == 4:
			tt = copy.copy(temp)
			c4 = re.compile('ldouOrigenX=([\-\d\.]+);var ldouOrigenY=([\-\d\.]+)')
			k = c4.findall(content)[0]
			tt.map = k[1]+','+k[0]
			#kk = station()
			#tt.insert()
			station_list.append(tt)
	return station_list

if __name__ == '__main__':
	print 'begin'
	it = station()
	it.url = 'http://www.metromadrid.es/en/viaja_en_metro/red_de_metro/lineas_y_horarios/index.html'
	it.Referer = 'http://www.metromadrid.es/en/viaja_en_metro/red_de_metro/'
	it.step = 1
	t = bfs(it)
	for i in t:
		i.showStation()
	print 'end'

