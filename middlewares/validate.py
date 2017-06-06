import aiohttp
import jsonschema

user_register = {
	"type" : "object",
	"required": ["firstname", "lastname", "email", "password"],
	"properties": {
		"firstname": { "type": "string", "maxLength": 15},
		"lastname": { "type": "string", "maxLength": 15},
		"email": { "type": "string", "format": "email", "maxLength": 30},
		"password": { "type": "string", "minLength": 4}
	}
}

user_login = {
	"type" : "object",
	"required": ["email", "password"],
	"properties": {
		"email": { "type": "string", "format": "email", "maxLength": 30},
		"password": { "type": "string" }
	}
}

user_reset = {
	"type" : "object",
	"required": ["email"],
	"properties": {
		"email": { "type": "string", "format": "email", "maxLength": 30}
	}
}

user_update = {
	"type" : "object",
	"properties": {
		"firstname": { "type": "string", "minLength": 2},
		"lastname": { "type": "string", "minLength": 2},
		"number": { "type": "string", "minLength": 11, "maxLength": 11},
		"image": { "type": "string",  "minLength": 50},
		"password": { "type": "string" }
	}
}

async def validateJson(app, handler):
	async def middleware_handler(request):
		try:
			
			if request.path == "/login" and request.method == "POST":
				body = await request.json()
				jsonschema.Draft4Validator(user_login).validate(body)
				return await handler(request)	
			elif request.path == "/register" and request.method == "POST":
				body = await request.json()
				jsonschema.Draft4Validator(user_register).validate(body)
				return await handler(request)
			elif request.path == "/reset" and request.method == "POST":
				body = await request.json()
				jsonschema.Draft4Validator(user_reset).validate(body)
				return await handler(request)
			elif request.path == "/" and request.method == "PATCH":
				body = await request.json()
				jsonschema.Draft4Validator(user_update).validate(body)
				return await handler(request)
			else:
				return await handler(request)
		except jsonschema.ValidationError as error:
			return aiohttp.web.json_response({"message": error.message}, status=400)
		except Exception as error:
			print({"type": "Error", "module": "Validate", "section": "validateJson", "message": error.message, "date": datetime.datetime.now().isoformat("T")})
			return aiohttp.web.json_response({"message": "Ошибка при валидации данных"},status=500)

	return middleware_handler
