#! /usr/bin/env python3
# -*-coding:utf-8 -*-


'''
Author:YoungRichOG
Hacking Everything :-)
2021/8/7
'''

import requests,urllib3,re
import concurrent.futures
import itertools
from bs4 import BeautifulSoup
from requests.packages import chardet

def _crateboomlist():
	protocols = ['http://','https://']
	_domainlist = open('domains.txt').read().splitlines()
	_iplist = open('ips.txt').read().splitlines()
	_xx = list(itertools.product(protocols,_iplist))
	_iplist = [i[0]+i[1] for i in _xx]
	_boomlist = list(itertools.product(_iplist,_domainlist))

	return _boomlist


def _boom(url):
	try:

		headers = {
			'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
		}
		r1 = requests.get(url[0],headers=headers,verify=False,timeout=5)
		charset = chardet.detect(r1.content)["encoding"]
		r1.encoding = charset
		soup1 = BeautifulSoup(r1.text, 'lxml')

		headers = {
			'Host': url[1],
			'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
		}

		r2 = requests.get(url[0],headers=headers,verify=False,timeout=5)
		charset = chardet.detect(r2.content)["encoding"]
		r2.encoding = charset
		soup2 = BeautifulSoup(r2.text, 'lxml')

		_data = url[0]+','+url[1]
		_data += ',原始标题:'+soup1.title.text+',原始长度:'+str(len(r1.content))+',变化长度:'+str(len(r2.content))
		_data += ',变化标题:'+soup2.title.text+',原始状态码:'+str(r1.status_code)+',变化状态码:'+str(r2.status_code)


		if soup2.title.text in _title_trigger:
			_title_trigger[soup2.title.text] += 1
			if _title_trigger[soup2.title.text] < 5 and url not in boooooom and soup1.title.text!= soup2.title.text:
				boooooom.append(_data)
		else:
			_title_trigger[soup2.title.text] = 0


		if len(r2.content) in _length_trigger:
			_length_trigger[len(r2.content)] +=1
			if _length_trigger[len(r2.content)] < 5 and url not in boooooom and len(r1.content)!= len(r2.content):
				boooooom.append(_data)
		else:
			_length_trigger[len(r2.content)] = 0


		if r2.status_code in _statuscode_trigger:
			_statuscode_trigger[r2.status_code] +=1
			if _statuscode_trigger[r2.status_code] < 5 and url not in boooooom and r1.status_code!= r2.status_code:
				boooooom.append(_data)
		else:
			_statuscode_trigger[r2.status_code] = 0


	except Exception as e:
		pass

if __name__ == '__main__':
	requests.packages.urllib3.disable_warnings()
	_title_trigger = {}
	_length_trigger = {}
	_statuscode_trigger = {}
	boooooom = []

	urls = _crateboomlist()

	with concurrent.futures.ThreadPoolExecutor(max_workers=200) as executor:
		_todo = {executor.submit(_boom,url): url for url in urls}
		for future in concurrent.futures.as_completed(_todo):
			url = _todo[future]

			data = future.result()
	print('YoungRichOG https://youngrichog.github.io/')
	print('-'*60)
	print('[**] 长度结果:',_length_trigger)
	print('[**] 标题结果:',_title_trigger)
	print('[**] 状态码结果:',_statuscode_trigger)
	print('-'*60)
	for res in set(boooooom):
		print(res)
		with open('boom.txt','a+') as file:
			file.write(res.rstrip()+'\n')