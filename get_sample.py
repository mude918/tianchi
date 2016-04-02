#!/usr/bin/env python
# coding=utf-8
import datetime

f = open("tianchi_fresh_comp_train_user.csv")
fs = open('data.csv', 'w')

#####   get data sample for demo
uid_set = []
cnt = 0
base_time = '2014-11-18'
for line in f:
	line = line.replace('\n', '')
	array = line.split(',')
	if array[0] == 'user_id':
		continue
	op_time = array[-1][0:10]
	d1 = datetime.datetime.strptime(base_time, "%Y-%m-%d")
	d2 = datetime.datetime.strptime(op_time, "%Y-%m-%d")
	diff_time = (d2 - d1).days
	newline = '%s,%s,%s,%s' %(array[0], array[1], array[2], diff_time)

	if array[0] in uid_set:
		fs.write(newline + '\n')
		continue
	elif cnt < 1000:
		uid_set.append(array[0])
		fs.write(newline + '\n')
		cnt += 1
	else:
		break