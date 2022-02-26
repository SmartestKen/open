import sys, aiohttp, aiofiles, json, asyncio, time
sys.path.append("/home/ken/private")
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib, mplcursors
matplotlib.use('GTK3Agg')
matplotlib.rcParams['font.size'] = 25

import plotly
pd.options.plotting.backend = "plotly"

from api_access import *
session = aiohttp.ClientSession()





async def generic_get(url, tempfile = "/tmp/data.html"):
	# get the url and return html
	# if cannot get sys.exit

	async with session.get(url) as response:
		html = await response.text()
		async with aiofiles.open(tempfile, mode='w')  as f:
			await f.write(html)
				
		if response.status == 200:
			return html
		else:
			sys.exit(html)



async def EOD_get_realtime_data(symbol_dict):


	symbol_list = [key for key in symbol_dict]
	slice_index = 0
	slice_len = 400
	bars_list = []
	while slice_index < len(symbol_list):
		
		slice_end = min(slice_index + slice_len, len(symbol_list))
		
		
		if slice_index != len(symbol_list) - 1:
			url = "https://eodhistoricaldata.com/api/real-time/" + symbol_list[0] + "?api_token=" + EOD_KEY + "&fmt=json&s=" + ",".join(symbol_list[slice_index:slice_end])
		else:
			url = "https://eodhistoricaldata.com/api/real-time/" + symbol_list[0] + "?api_token=" + EOD_KEY + "&fmt=json"
		html = await generic_get(url)
		temp = json.loads(html)
		for i in range(len(temp)):
			temp[i]["name"] = symbol_dict[temp[i]["code"]]
		bars_list += temp
		
		slice_index += slice_len
		print(bars_list)
	
		
	temp_df = pd.DataFrame(bars_list, index = list(range(len(bars_list))))
	
	return temp_df[temp_df["change_p"] != "NA"]


async def EOD_get_intraday_data(start, symbol_list):
	bars_list = []
	for symbol in symbol_list:
		url = "https://eodhistoricaldata.com/api/intraday/" + symbol + "?api_token=" + EOD_KEY + "&fmt=json&interval=30m&from=" + start
		html = await generic_get(url)
		# print(html)
		bars_list.append(json.loads(html))
		
	# print(bars_list)
	return bars_list

# return a dictionary with key = code and value = country + name
async def EOD_get_indices_dict():
	url = "https://eodhistoricaldata.com/api/exchange-symbol-list/INDX?api_token=" + EOD_KEY + "&fmt=json"
	html = await generic_get(url)
	indices_dict = dict()
	for item in json.loads(html):
		indices_dict[item['Code'] + ".INDX"] = item['Country'] + " " + item['Name']

	return indices_dict







# install pygobject, pycairo
# paccman -S gobject-introspection
async def EOD_plot(symbol_list, bars_list):
	
	merged_df = None
	xlabel = "datetime"
	ylabel = "close"
	available_symbol_list = []
	for index, bars in enumerate(bars_list):
		if bars == []:
			continue
		else:
			available_symbol_list.append(symbol_list[index])
			
		df = pd.DataFrame.from_dict(bars)
		# print(df)
		
		if len(available_symbol_list) == 1:
			# the first symbol with non-empty bars
			merged_df = df[[xlabel, ylabel]]
			merged_df.rename(columns={ylabel: symbol_list[index]}, inplace=True)
		else:
			temp = df[[xlabel, ylabel]]
			temp.rename(columns={ylabel: symbol_list[index]}, inplace=True)
			merged_df = pd.merge(merged_df, temp, how="outer", on=[xlabel])
	
	merged_df.interpolate(inplace=True)	
	print(merged_df)
	
	ax = None
	for index, symbol in enumerate(available_symbol_list):
		if index == 0:
			ax = merged_df.plot(x = xlabel, y = symbol)
		else:
			ax = merged_df.plot(x = xlabel, y = symbol, ax = ax)
		
	'''
	cursor = mplcursors.cursor(ax, hover=True)	
	cursor.connect('add', show_annotation)
	plt.legend(loc="best")
	plt.show()
	'''
	
	ax.update_layout(
    title="Plot Title",
    xaxis_title="time",
    yaxis_title="level",
    legend_title="Legend Title",
    font=dict(
        family="Courier New, monospace",
        size=25,
        color="RebeccaPurple"))
	ax.show()

		
loop = asyncio.get_event_loop()
# = ["000906.INDX", "GSPC.INDX", "BCOMCL.INDX"]
import csv

with open("/home/") as fp:
    reader = csv.reader(fp, delimiter=",", quotechar='"')

	index = 0
    for row in reader:
		print(row)
		if index > 10:
			break
		else:
			index += 1
		




'''
symbol_dict = loop.run_until_complete(loop.create_task(EOD_get_indices_dict()))


bars_df = loop.run_until_complete(loop.create_task(EOD_get_realtime_data(symbol_dict)))
bars_df.sort_values("change_p")[["code", "name", "close", "previousClose", "change_p"]].to_csv("/home/ken/Downloads/etf_return_sorted", index = False)

sys.exit(0)
time.sleep(100000)

ax = bars_df.sort_values("change_p").plot(x = "code", y = "change_p")	
ax.update_layout(
title="Plot Title",
xaxis_title="time",
yaxis_title="level",
legend_title="Legend Title",
font=dict(
	family="Courier New, monospace",
	size=25,
	color="RebeccaPurple"))
ax.show()




# bars_list = loop.run_until_complete(loop.create_task(EOD_get_data("1641024000", symbol_list)))
# https://eodhistoricaldata.com/api/exchanges-list/?api_token=YOUR_API_TOKEN&fmt=json
# bars = loop.run_until_complete(loop.create_task(EOD_plot(symbol_list, bars_list)))
'''
loop.run_until_complete(loop.create_task(session.close()))
