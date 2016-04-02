#!/usr/bin/env python
# coding=utf-8
import math
import numpy as np

sample_size = 2000
block = 10
path2 = []
path3 = []
f = []
wf = []
for idx in range(block):
	path2.append(r'data_%s_%s.csv' %(sample_size, idx))
	path3.append(r'ans_%s_%s.csv' %(sample_size, idx))
	f.append(open(path2[idx]))
	wf.append(open(path3[idx], 'w'))


	####   underline check, dwindow = 1                        ####
	####   use (user_id, item_id, 29) to train                 ####
	####   use (user_id, item_id, 30) as offline_candidate     ####
	####   use (user_id, item_id, 31) as online_candidate      ####

	### (user_id, item_id, act_day)
	### x_feature
	### y_label

	train_day29 = []
	offline_candidate_day30 = []
	online_candidate_day31 = []

	#for demo, for this feature, sum of 4 operations
	ui_dict = [{} for i in range(4)]

	#for buy label
	ui_buy = {}

	#with open("data.csv") as context:
	for line in f[idx]:
		line = line.replace('\n', '')
		array = line.split(',')
		if array[0] == 'user_id':
			continue

		day = int(array[-1])

		uid = (array[0], array[1], day)
		#for buy label
		if array[2] == '4':
			ui_buy[uid] = 1;
		#for demo, for this feature, sum of 4 operations
		act_type = int(array[2]) - 1
		if uid in ui_dict[act_type]:
			ui_dict[act_type][uid] += 1
		else:
			ui_dict[act_type][uid] = 1

		#data for predict
		uid = (array[0], array[1], day + 1)
		if day == 28:
			train_day29.append(uid)
		if day == 29:
			offline_candidate_day30.append(uid)
		if day == 30:
			online_candidate_day31.append(uid)

	###remove duplicate
	train_day29 = list(set(train_day29))
	offline_candidate_day30 = list(set(offline_candidate_day30))
	online_candidate_day31 = list(set(online_candidate_day31))


	print 'training item number:\t', len(train_day29)
	print '---------------------\n'
	print 'offline candidate item number:\t', len(offline_candidate_day30)
	print '---------------------\n'

	#########################



	#get train x,y
	x = np.zeros((len(train_day29), 4))
	y = np.zeros((len(train_day29)), )
	id = 0
	for uid in train_day29:
		last_uid = (uid[0], uid[1], uid[2] - 1)
		for i in range(4):
			x[id][i] = math.log1p(ui_dict[i][last_uid] if last_uid in ui_dict[i] else 0)
		y[id] = 1 if uid in ui_buy else 0
		id += 1


	print 'x = ', x, '\n\n', 'y = ', y
	print '-------------------\n\n'
	print 'train number = ', len(y), '\n', 'positive number = ', sum(y), '\n'

	### get predict px for offline_candidate_day30
	px = np.zeros((len(offline_candidate_day30), 4))
	id = 0
	for uid in offline_candidate_day30:
		last_uid = (uid[0], uid[1], uid[2] - 1)
		for i in range(4):
			px[id][i] = math.log1p(ui_dict[i][last_uid] if last_uid in ui_dict[i] else 0)
		id += 1


	### same to online_candidate_day31  









	#### training #########################################
	#from sklearn.tree import DecisionTreeClassifier
	#from sklearn.ensemble import RandomForestClassifier
	from sklearn.linear_model import LogisticRegression
	model = LogisticRegression()
	#model = DecisionTreeClassifier(max_depth = 4)
	#model = RandomForestClassifier()
	model.fit(x, y)


	### evaluate ##########################################
	py = model.predict_proba(px)
	npy = []
	for a in py:
		npy.append(a[1])
	py = npy

	print 'px = '
	print px

	### combine
	lx = zip(offline_candidate_day30, py)
	#print lx
	print '---------------------'
	## sort by predict score
	lx = sorted(lx, key = lambda x:x[1], reverse = True)
	#print lx
	print '---------------------'

	#path3 = 'ans_%s.csv' %(sample_size)

	for i in range(874):
		item = lx[i]
		wf[idx].write('%s,%s\n'%(item[0][0], item[0][1]))