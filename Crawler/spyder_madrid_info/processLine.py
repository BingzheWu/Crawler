#!/usr/bin/env python
#-*- coding:utf-8 -*-

import re
from traffic_class import line, route, station
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def f(a,b):
	t1 = int(a.split('|')[-1])
	t2 = int(b.split('|')[-1])
	return t1 - t2


def dosth(fp):
	res_list = []
	line_dict = {}
	r = open(fp,'r')
	cp = re.compile('self\.name = ([^,]+),.*self\.map = (\d+\.\d+,\-?\d+\.\d+),.*self\.line = ([^,]+),.*self\.num = (\d+),')
	for line1 in r:
		t = cp.findall(line1)[0]
		res_list.append(t)
	for i in res_list:
		if line_dict.get(i[2]):
			line_dict[i[2]].append('|'.join(i))
		else:
			line_dict[i[2]] = [ '|'.join(i) ]
	
	res_list = []
	for key,value in line_dict.items():
		t = value
		t.sort(cmp = f)
		Line = line()
		Line.set_data(line_name = key.replace(' ','',100) )
		Route = route(Line)
		Route.set_data(route_name = key.replace(' ','',100))
		time = '###[INTERVAL][MON~FRI:6.05~7.00:6][MON~FRI:7.00~9.30:4][MON~FRI:9.30~21.00:5][MON~FRI:21.00~23.00:8][MON~FRI:23.00~23.59:15][MON~FRI:0.01~2.00:15][SAT:6.05~18.00:8][SAT:18.00~21.00:5][SAT:21.00~22.00:7][SAT:22.00~23.00:9][SAT:23.00~23.59:10][SAT:0.01~2.00:15][SUN:6.05~21.30:8][SUN:21.30~23.00:9][SUN:23.00~23.59:15][SUN:0.01~2.00:15]'
		Route.set_time( time = time)
		for i in t:
			Station = station()
			Station.map_info = i.split('|')[1]
			Station.station_name = i.split('|')[0]
			Station.station_num = i.split('|')[-1]
			Station.station_run_time = (int(i.split('|')[-1])-1) * 2
			Route.append_station(Station)
		res_list.append( Route.show_stations())
		res_list.append( Route.get_reverse_route())


	return res_list


if __name__ == '__main__' :
	fp = sys.argv[1]
	t = dosth(fp)
	for i in t:
		print i
