from aiohttp import web
from utils.metrics import registry, generate_latest

async def showMetrics(request):
	try:
		return web.Response(body=generate_latest(registry=registry))
	except:
		return web.Response(status=500)