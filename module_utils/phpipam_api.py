import requests
import json
from ansible.errors import AnsibleError
class API:
	def __init__(self, username,password,server):
		response = requests.post(server+"/user/",auth=(username,password))
		if response.status_code != 200:
			raise AnsibleError('phpipam authentication failed')
		self.server = server
		self.auth = response.json()['data']['token']

	def php_ipam_request(self,request_type,api_endpoint,**kwargs):
		try:
			if request_type != "get" and request_type != 'delete':
				response = getattr(requests,request_type)(self.server+"/"+api_endpoint,data=json.dumps(kwargs['data']),headers={'phpipam-token':self.auth})
			else:
				response = getattr(requests,request_type)(self.server+"/"+api_endpoint,headers={'phpipam-token':self.auth})
			if response.status_code not in range(200,300):
				raise AnsibleError('phpipam call failed with {code}: {message}'.format(code=response.status_code,
					message=response.json()['message']))
			return response.json()
		except Exception as error:
			raise AnsibleError(str(error))

	
	#Be careful with this and make sure you clean the data before putting stuff in
	#EX:don't pass in "lastDiscovery" from the subnet info
def is_different(new_data,old_data):
	if len(set(new_data.values()).diffence(old_data.values())) > 0:
		return True
	else:
		return False

def get_params(module_params,request_data):
	new_data = {}
	new_module_params = {}
	for key in module_params.keys():
		if module_params[key]:
			new_data[key] = request_data[key]
			new_module_params = module_params[key]
	return new_data, new_module_params

def convert_bools(module_params):
	new_module_params = {}
	for key in module_params.keys():
		if module_params[key] == True:
			new_module_params[key] = "1"
		elif module_params[key] == False:
			new_module_params[key] = "0"
		else:
			new_module_params[key] = module_params[key]
	return new_module_params

def clean_post_values(module_params,values):
	new_module_params = {}
	for key in module_params.keys():
		if key not in values:
			if module_params[key]:
				new_module_params[key] = module_params[key]
	return new_module_params