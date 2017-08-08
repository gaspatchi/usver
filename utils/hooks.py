import datetime
import sys
import consul
import hvac
import tarantool
from utils.config import config

def setTarantool(consulConnection):
	tarantoolInfo = consulConnection.catalog.service("tarantool")
	if len(tarantoolInfo[1]) != 0:
		config["tarantool"]["address"] = tarantoolInfo[1][0]["ServiceAddress"]
		config["tarantool"]["port"] = tarantoolInfo[1][0]["ServicePort"]
	else:
		print({"type": "Fatal", "module": "Init", "section": "setTarantool", "message": "Сервис Tarantool недоступен", "date": datetime.datetime.now().isoformat("T")})
		raise Exception("Сервис Tarantool недоступен")

def setTokenzer(consulConnection):
	tokenzerInfo = consulConnection.catalog.service("tokenzer")
	if len(tokenzerInfo[1]) != 0:
		config["tokenzer"]["address"] = tokenzerInfo[1][0]["ServiceAddress"]
		config["tokenzer"]["port"] = tokenzerInfo[1][0]["ServicePort"]
	else:
		print({"type": "Fatal", "module": "Init", "section": "setTokenzer", "message": "Сервис Tokenzer недоступен", "date": datetime.datetime.now().isoformat("T")})
		raise Exception("Сервис Tokenzer недоступен")

async def registerService(app):
	try:
		consulConnection = consul.Consul(host=config["consul"]["address"],port=config["consul"]["port"])
		consulConnection.agent.service.register(config["server"]["name"],address=config["server"]["address"],port=config["server"]["port"])
		setTokenzer(consulConnection)
		setTarantool(consulConnection)
		app["tarantool"] = tarantool.connect(host=config["tarantool"]["address"],port=config["tarantool"]["port"], user=config["tarantool"]["user"], password=config["tarantool"]["password"])
	except Exception as error:
		print({"type": "Fatal", "module": "Init", "section": "registerService", "message": error.__str__(), "date": datetime.datetime.now().isoformat("T")})
		consulConnection.agent.service.deregister(config["server"]["name"])
		sys.exit("Невозможно получить информацию о сервисах")

async def shutdowService(app):
	consulConnection = consul.Consul()
	consulConnection.agent.service.deregister(config["server"]["name"])