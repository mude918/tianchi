#!/usr/bin/env python
# coding=utf-8
import sys

sample_size = 2000
block = 10
path1 = []
st = []
F1 = []
SF1 = []
path4 = []
f = []
sa = 0
sb = 0
sc = 0

for idx in range(block):
	path1.append(r'offline_ground_truth_%s_%s.csv' %(sample_size, idx))
	path4.append(r'ans_%s_%s.csv' %(sample_size, idx))
	st.append(open(path1[idx]))
	#const = st.readlines()

	answer = []

	for a in st[idx]:
		if a[0] == 'u':
			continue
		answer.append(a)
	answer = set(answer)

	f.append(open(path4[idx]))
	#con = f.readlines()
	you = []
	for a in f[idx]:
		if a[0] == 'u':
			continue
		you.append(a)
	you = set(you)

	inter = answer & you
	print 'hit number: ', len(inter)

	if len(inter) > 0:
		a = len(answer)
		sa += a
		b = len(you)
		sb += b
		c = len(inter)
		sc += c
		R = 1.0 * c / a * 100
		P = 1.0 * c / b * 100
		SR = 1.0 * sc / sa * 100
		SP = 1.0 * sc / sb * 100
		F1.append(2.0 * R * P / (R + P))
		SF1.append(2.0 * SR * SP / (SR + SP))
		print '%s block:F1/R/P %.2f%%/%.2f%%/%.2f%%/\n' % (idx, F1[idx], R, P)
		print 'all block:F1/R/P %.2f%%/%.2f%%/%.2f%%/\n' % (SF1[idx], SR, SP)