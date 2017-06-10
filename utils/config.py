import os
config = {
	"server": {
		"name": "usver",
		"address": "127.0.0.1",
		"port": 8080,	
	},
	"tarantool": {
		"address": "",
		"port": "",
		"user": os.environ.get("tarantool_user"),
		"password": os.environ.get("tarantool_password")
	},
	"tokenzer": {
		"address": "",
		"port": ""	
	}
}