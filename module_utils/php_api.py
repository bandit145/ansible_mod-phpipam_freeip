import requests
import json
class API:
	def __init__(username,password,server):
		response = requests.post(server,auth=(username,password))
		self.server = server
		self.auth = response.headers['phpipam-token']

	def php_ipamrequest(request_type,data,body):
		try:
			getattr(requests,request_type)(self.server,data=json.dumps(data),headers={'phpipam-token':self.auth})

		except Exception as error:
			print
