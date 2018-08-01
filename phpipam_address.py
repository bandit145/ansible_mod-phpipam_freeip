#!/usr/bin/env python
from ansible.module_utils.basic import *
from ansible.module_utils.phpipam_api import *
import sys
import os


def get_subnet(subnet_cidr, phpipam, module):
	subnet = phpipam.php_ipam_request('get','subnets/cidr/'+module.params['subnet'])
	if subnet['success'] != True:
		module.fail_json(msg='Subnet with that cidr does not exist!')
	return subnet['data'][0]['id']


def ensure(module):
	phpipam = API(module.params['username'],module.params['password'],module.params['ipam_host'])
	address_response = phpipam.php_ipam_request('get','addresses/search/'+module.params['ip'])
	if address_response['success'] != 0:
		ip_address,module_params = get_params(module.params,addresses_response['data'][0],['subnetId'])
		if is_different(ip_address,module_params):
			module_params['subnetId'] = get_subnet(module.params['subnet'],phpipam,module)
			phpipam.php_ipam_request('patch','addresses/'+ip_address['id']+'/',data=module_params)
			module.exit_json(changed=True)
	elif address_response['success'] == 0:
		module_params = convert_bools(module.params)
		#remove errant params
		module_params['subnetId'] = get_subnet(module.params['subnet'],phpipam,module)
		module.fail_json(msg=module_params)
		phpipam.php_ipam_request('post','addresses/',data=module_params)
		module.exit_json(changed=True)
	else:
		module.exit_json(changed=False)



def main():
	module = AnsibleModule(
			argument_spec = dict(
				ipam_host = dict(type=str,required=True),
				ip = dict(type=str,required=True,aliases=['ip_address']),
				subnet = dict(type=str,required=True),
				description = dict(type=str,required=False),
				hostname = dict(type=str,required=False),
				mac = dict(type=str,required=False),
				owner = dict(type=str,required=False),
				PTRignore = dict(type=bool,required=False,aliases=['ptr_ignore']),
				PTR = dict(type=bool,required=False, aliases=['ptr']),
				note = dict(type=str,required=False),
				is_gateway = dict(type=str,required=False),
				exclude_ping = dict(typ=bool,required=False),
				username = dict(type=str,required=True),
				password = dict(type=str,required=True),
				validate_certs = dict(type=str,choices=[True,False],default=True),
			),
			supports_check_mode=False
	)
	ensure(module)

if __name__ == '__main__':
	main()