import datetime
import sys
import consul
import hvac
import tarantool
from utils.config import config


def setTarantool(consulConnection, client):
	tarantoolInfo = consulConnection.catalog.service("tarantool")
	if len(tarantoolInfo[1]) != 0:
		config["tarantool"]["address"] = tarantoolInfo[1][0]["ServiceAddress"]
		config["tarantool"]["port"] = tarantoolInfo[1][0]["ServicePort"]
		tarantool_user = client.read("secret/tarantool/user")
		tarantool_password = client.read("secret/tarantool/password")
		config["tarantool"]["user"] = tarantool_user["data"]["value"]
		config["tarantool"]["password"] = tarantool_password["data"]["value"]
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

def setVault(consulConnection):
	vaultInfo = consulConnection.catalog.service("vault")
	if len(vaultInfo[1]) != 0:
		config["vault"]["address"] = vaultInfo[1][0]["ServiceAddress"]
		config["vault"]["port"] = vaultInfo[1][0]["ServicePort"]
	else:
		print({"type": "Fatal", "module": "Init", "section": "setVault", "message": "Сервис Vault недоступен", "date": datetime.datetime.now().isoformat("T")})
		raise Exception("Сервис Vault недоступен")

async def registerService(app):
	try:
		consulConnection = consul.Consul()
		consulConnection.agent.service.register("usver",address=config["server"]["address"],port=config["server"]["port"])
		setVault(consulConnection)
		client = hvac.Client(url="http://{0}:{1}".format(config["vault"]["address"],config["vault"]["port"]),token=config["vault"]["token"],timeout=2)
		setTokenzer(consulConnection)
		setTarantool(consulConnection, client)
		app["tarantool"] = tarantool.connect(host=config["tarantool"]["address"],port=config["tarantool"]["port"], user=config["tarantool"]["user"], password=config["tarantool"]["password"])
	except Exception as error:
		print({"type": "Fatal", "module": "Init", "section": "registerService", "message": error.message, "date": datetime.datetime.now().isoformat("T")})
		consulConnection.agent.service.deregister("usver")
		sys.exit("Невозможно получить информацию о сервисах")

async def shutdowService(app):
	consulConnection = consul.Consul()
	consulConnection.agent.service.deregister("usver")
