import sys, aiohttp, aiofiles, json, asyncio, time
sys.path.append("/home/ken/private")
from api_access import *




session = aiohttp.ClientSession()
loop = asyncio.get_event_loop()


# get the url and return html
# if cannot get sys.exit
async def generic_get(url, tempfile = "/tmp/data.html"):

	async with session.get(url) as response:
		html = await response.text()
		async with aiofiles.open(tempfile, mode='w')  as f:
			await f.write(html)
				
		if response.status == 200:
			return html
		else:
			sys.exit(html)

# expect start format 'YY-MM-DD'
# start-end max 3600 days
async def EOD_get_data(start, symbol):

	url = "https://eodhistoricaldata.com/api/eod/" + symbol + "?api_token=" + EOD_KEY + "&fmt=json&interval=30m&from=" + start
	
	html = await generic_get(url)
	return json.loads(html)




# --------------------load news data
import csv

if len(sys.argv) == 1:
	sys.exit("Need an argument of news data file")

news_dict = dict()
with open(sys.argv[1]) as fp:
	reader = csv.DictReader(fp, delimiter=",", quotechar='"')
	
	index = 0
	for line in enumerate(reader):
		if index > 30000:
			break
		else:
			index += 1
		# print(line[1]["headline"], line[1]["date"])
		# print(line[1]["date"])
		news_dict[line[1]["date"].split()[0]] = news_dict.get(line[1]["date"].split()[0], "") + "\n" + line[1]["headline"]

# --------------------load time series data
symbol = "GSPC.INDX"
bars_list = loop.run_until_complete(loop.create_task(EOD_get_data("2010-01-01", symbol)))
# bars_list = loop.run_until_complete(loop.create_task(EOD_get_intraday_data("2018-01-01 00:00:00", "2022-01-01 00:00:00", symbol_list)))


# 1. concat news of the day
# 2. ignore those not in the trading day

indices = dict()
for index, bar in enumerate(bars_list):
	indices[bar['date']] = index


import numpy


positive = 0
negative = 0
for date in news_dict:
	if indices.get(date, None) != None:
		bar = bars_list[indices[date]]
		volatility = numpy.std([bar['open'], bar['close'], bar['high'], bar['low']])
		if date in ["2020-05-12", "2020-05-15", "2020-05-18", "2020-06-01"]:
			print(date, round(volatility,3))
			print(news_dict[date])
		if volatility > 10:
			positive += 1
		else:
			negative += 1
print(positive/(positive + negative))


loop.run_until_complete(loop.create_task(session.close()))
