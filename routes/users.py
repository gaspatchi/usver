import datetime
import aiohttp
from utils.config import config
from utils.metrics import (advents_profile, advents_time, change_time,
                           changes_profile, completed_verification, login_time,
                           logins_sum, password_resets, registration_time,
                           reset_time, sum_users, verification_time)


@registration_time.time()
async def registerUser(request):
	try:
		body = await request.json()
		response = request.app["tarantool"].call("registerUser", body["email"], body["firstname"], body["lastname"], body["password"])
		if response[0][0] == True:
			sum_users.inc()
			return aiohttp.web.json_response({"message": response[1][0]}, status=200)
		elif response[0][0] == False:
			return aiohttp.web.json_response({"message": response[1][0]}, status=409)
	except Exception as error:
		print({"type": "Error", "module": "Users", "section": "registerUser", "message": error.__str__(), "date": datetime.datetime.now().isoformat("T")})
		return aiohttp.web.json_response({"message": "Невозможно выполнить регистрацию"}, status=500)

@verification_time.time()
async def verifyToken(request):
	try:
		response = request.app["tarantool"].call("completeVerification", request.match_info.get("token"))
		if response[0][0] == True:
			completed_verification.inc()
			return aiohttp.web.json_response({"message": response[1][0]}, status=200)
		elif response[0][0] == False:
			return aiohttp.web.json_response({"message": response[1][0]}, status=404)
	except Exception as error:
		print({"type": "Error", "module": "Users", "section": "verifyToken", "message": error.__str__(), "date": datetime.datetime.now().isoformat("T")})
		return aiohttp.web.json_response({"message": "Невозможно выполнить верификацию"}, status=500)

@login_time.time()
async def loginUser(request):
	try:
		body = await request.json()
		response = request.app["tarantool"].call("loginUser",body["email"],body["password"])
		if response[0][0] == True:
			async with aiohttp.ClientSession() as session:
				async with session.post("http://{0}:{1}/create".format(config["tokenzer"]["address"],config["tokenzer"]["port"]),json=response[1][0]) as response:
					if response.status == 200:
						logins_sum.inc()
						return aiohttp.web.json_response(await response.json(), status=200)
					else:
						return aiohttp.web.json_response(await response.json(), status=response.status)
		elif response[0][0] == False:
			return aiohttp.web.json_response({"message": response[1][0]}, status=404)
	except Exception as error:
		print({"type": "Error", "module": "Users", "section": "loginUser", "message": error.__str__(), "date": datetime.datetime.now().isoformat("T")})
		return aiohttp.web.json_response({"message": "Невозможно выполнить вход"}, status=500)

@reset_time.time()
async def resetPassword(request):
	try:
		body = await request.json()
		response = request.app["tarantool"].call("resetPassword", body["email"])
		if response[0][0] == True:
			password_resets.inc()
			return aiohttp.web.json_response({"message": response[1][0]}, status=200)
		elif response[0][0] == False:
			return aiohttp.web.json_response({"message": response[1][0]}, status=404)		
	except Exception as error:
		print({"type": "Error", "module": "Users", "section": "resetPassword", "message": error.__str__(), "date": datetime.datetime.now().isoformat("T")})
		return aiohttp.web.json_response({"message": "Невозможно сбросить пароль"}, status=500)

@advents_time.time()
async def selectProfile(request):
	try:
		response = request.app["tarantool"].call("selectUser",request["profile"]["sub"])
		if response[0][0] == True:
			advents_profile.inc()
			return aiohttp.web.json_response(response[1][0], status=200)
		elif response[0][0] == False:
			return aiohttp.web.json_response({"message": response[1][0]}, status=404)		
	except Exception as error:
		print({"type": "Error", "module": "Users", "section": "selectProfile", "message": error.__str__(), "date": datetime.datetime.now().isoformat("T")})
		return aiohttp.web.json_response({"message": "Невозможно получить профиль"}, status=500)

@change_time.time()
async def updateProfile(request):
	try:
		body = await request.json()
		response = request.app["tarantool"].call("updateUser",request["profile"]["sub"], body.get("firstname",None),\
		body.get("lastname",None),body.get("number",None),body.get("image",None),body.get("password",None))
		if response[0][0] == True:
			changes_profile.inc()
			return aiohttp.web.json_response({"message": response[1][0]}, status=200)
		elif response[0][0] == False:
			return aiohttp.web.json_response({"message": response[1][0]}, status=404)		
	except Exception as error:
		print({"type": "Error", "module": "Users", "section": "updateProfile", "message": error.__str__(), "date": datetime.datetime.now().isoformat("T")})
		return aiohttp.web.json_response({"message": "Невозможно получить профиль"}, status=500)