import os
import pandas
import json
if os.path.exists('link.csv'):
	links = []
	file = open('link.csv')
	link_list = file.readlines()
	link_list = link_list[1:]
	for link in link_list:
		print(link)
		link = list(map(int, (link[: -1]).split(',')))[1: ]
		links.append(link)
		print(link)

# file = open('path/result_20201116_032636.json')
# r = file.read()
# r = json.loads(r)
# methods = []
# keys = r.keys()
# for key in keys:
# 	methods.append({key : r[key]})
# print(methods)