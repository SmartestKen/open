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

# expect start format '%Y-%m-%d %H:%M:%S'
async def EOD_get_intraday_data(start, end, symbol_list):
	# convert to epoch
	start = str(int(time.mktime(time.strptime(start, '%Y-%m-%d %H:%M:%S'))))

	bars_list = []
	for symbol in symbol_list:
		url = "https://eodhistoricaldata.com/api/intraday/" + symbol + "?api_token=" + EOD_KEY + "&fmt=json&interval=30m&from=" + start
		html = await generic_get(url)
		# print(html)
		bars_list.append(json.loads(html))
		
	# print(bars_list)
	return bars_list
	
	
symbol_list = ["GSPCC.INDX"]
bars_list = loop.run_until_complete(loop.create_task(EOD_get_intraday_data("2010-01-01 00:00:00", symbol_list)))
print(bars_list)
