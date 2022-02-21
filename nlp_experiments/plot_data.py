import sys, aiohttp, aiofiles, json, asyncio
sys.path.append("/home/ken/private")

from api_access import *
session = aiohttp.ClientSession()

async def generic_get(url):
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



async def EOD_get_data(start, symbol, tempfile = "/tmp/data.html"):
	url = "https://eodhistoricaldata.com/api/eod/" + symbol + suffix + "?api_token=" + EOD_KEY + "&fmt=json&from=" + http_start + "&to=" + end
	html = await generic_get(url)
	return json.load(html)



		
loop = asyncio.get_event_loop()
bars = loop.run_until_complete(loop.create_task(EOD_get_data("GSPC.INDX", "1y")))



https://eodhistoricaldata.com/api/exchanges-list/?api_token=YOUR_API_TOKEN&fmt=json
1y 1m 1w today
print(bars)
loop.run_until_complete(loop.create_task(session.close()))
