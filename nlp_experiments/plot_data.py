import sys, aiohttp, aiofiles, json, asyncio
sys.path.append("/home/ken/private")

from api_access import *
session = aiohttp.ClientSession()




async def EOD_get_data(start, symbol, tempfile = "/tmp/data.html"):
	url = "https://eodhistoricaldata.com/api/eod/" + symbol + "?api_token=" + EOD_KEY + "&fmt=json&from=" + start

	async with session.get(url) as response:
		html = await response.text()
		async with aiofiles.open(tempfile, mode='w')  as f:
			await f.write(html)
				
		if response.status == 200:
			return json.loads(html)
		else:
			sys.exit(html)
		
		
loop = asyncio.get_event_loop()
bars = loop.run_until_complete(loop.create_task(EOD_get_data("GSPC.INDX", "1y")))

1y 1m 1w today
print(bars)
loop.run_until_complete(loop.create_task(session.close()))
