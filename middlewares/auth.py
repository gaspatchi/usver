import re
import time
import aiohttp
from utils.config import config
from utils.metrics import checked_tokens, tokenzer_reply

regex = re.compile("Bearer\s(\S+)")

async def verifyAuth(app, handler):
	async def middleware_handler(request):
		try:
			if request.path == "/":
				checked_tokens.inc()
				header = regex.findall(request.headers.get("Authorization"))
				if len(header) != 0:
					start = time.perf_counter()
					async with aiohttp.ClientSession(conn_timeout=2,read_timeout=2) as session:
						async with session.post("http://{0}:{1}/verify".format(config["tokenzer"]["address"],config["tokenzer"]["port"]),json={"token": header[0]}) as response:
							tokenzer_reply.set(time.perf_counter()- start)
							if response.status == 200:
								request["profile"] = await response.json()
								return await handler(request)
							else:
								return aiohttp.web.json_response(await response.json(), status=403)	
				else:
					return aiohttp.web.json_response({"message": "Неверный заголовок"}, status=403)
			else:
				return await handler(request)
		except aiohttp.ClientError:
			return aiohttp.web.json_response({"message": "Невозможно проверить сессию"}, status=500)
	return middleware_handler
