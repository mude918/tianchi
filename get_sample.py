#!/usr/bin/env python
# coding=utf-8
import datetime
import os

sample_size = 2000
block = 10
path1 = []
path2 = []
st = []
fs = []
for i in range(block):
	path1.append(r'offline_ground_truth_%s_%s.csv' %(sample_size, i))
	path2.append(r'data_%s_%s.csv' %(sample_size, i))

if not os.path.exists(path2[block-1]):
	f = open('tianchi_fresh_comp_train_user.csv')
	for i in range(block):
		st.append(open(path1[i], 'w'))
		fs.append(open(path2[i], 'w'))

	#####   get data sample for demo
	uid_set = []
	cnt = 0
	i = 0
	base_time = '2014-11-18'
	for line in f:
		line = line.replace('\n', '')
		array = line.split(',')
		if array[0] == 'user_id':
			continue
		if i < block:
			op_time = array[-1][0:10]
			d1 = datetime.datetime.strptime(base_time, "%Y-%m-%d")
			d2 = datetime.datetime.strptime(op_time, "%Y-%m-%d")
			diff_time = (d2 - d1).days
			newline = '%s,%s,%s,%s' %(array[0], array[1], array[2], diff_time)
			if array[0] in uid_set:
				fs[i].write(newline + '\n')
				if diff_time == 30 and array[2] =='4':
					stline = '%s,%s' %(array[0], array[1])
					st[i].write(stline + '\n') 
				continue
			elif cnt < sample_size:
				uid_set.append(array[0])
				fs[i].write(newline + '\n')
				cnt += 1
				if diff_time == 30 and array[2] =='4':
					stline = '%s,%s' %(array[0], array[1])
					st[i].write(stline + '\n') 
			else:
				fs[i].flush()
				st[i].flush()
				uid_set = []      #only when the uid is ordered
				cnt = 0
				i += 1
		else:		
			break