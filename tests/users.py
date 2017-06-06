import unittest
import requests

class TestValideUserService(unittest.TestCase):
	token = ""

	def setUp(self):
		self.host = "http://127.0.0.1"
		
		self.register_profile = {
		"firstname": "Никита",
		"lastname": "Бережной",
		"email": "nikitoshi@test.ru",
		"password": "13371488"
		}

		self.login_profile = {
		"firstname": "Никита",
		"lastname": "Бережной",
		"email": "nikitoshi@gaspatchi.ru",
		"password": "13371488"
		}

	
	def test_register(self):
		result = requests.post("{0}/user/register".format(self.host),json=self.register_profile)
		body = result.json()
		self.assertEqual(result.status_code,200)
		self.assertIn("message",body)	
	
	def test_login(self):
		result = requests.post("{0}/user/login".format(self.host),json=self.login_profile)
		body = result.json()
		self.assertEqual(result.status_code,200)
		self.assertIn("token",body)
		self.__class__.token = body["token"]
	
	def test_select(self):
		result = requests.get("{0}/user".format(self.host),headers={"Authorization": "Bearer {0}".format(self.token)})
		body = result.json()
		self.assertEqual(result.status_code,200)
		self.assertIn("info",body)
		self.assertIn("subscription",body)

class TestInvalideUserService(unittest.TestCase):
	def setUp(self):
		self.host = "http://127.0.0.1"
		
		self.register_profile = {
		"firtname": "Никита",
		"lastname": "Бережной",
		"email": "nikitoshi@test.ru",
		"passord": "13371488"
		}

		self.login_profile = {
		"firstname": "Никита",
		"lastname": "Бережной",
		"mail": "nikitoshi@gaspatchi.ru",
		"password": ""
		}

	def test_register(self):
		result = requests.post("{0}/user/register".format(self.host),json=self.register_profile)
		body = result.json()
		self.assertEqual(result.status_code,400)
		self.assertIn("message",body)
	
	
	def test_login(self):
		result = requests.post("{0}/user/login".format(self.host),json=self.login_profile)
		body = result.json()
		self.assertEqual(result.status_code,400)
		self.assertIn("message",body)
	
	def test_select(self):
		result = requests.get("{0}/user".format(self.host),headers={"Authorization": "Bearer {0}".format(self.token)})
		self.assertEqual(result.status_code,403)
		self.assertIn("message",body)