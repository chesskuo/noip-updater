import argparse
import requests
import platform

url = {
	'v4_ori': 'http://ip1.dynupdate.no-ip.com/',
	'v4_bak': 'http://ip1.dynupdate.no-ip.com:8245/',
	'v6_ori': 'http://ip1.dynupdate6.no-ip.com/',
	'v6_bak': 'http://ip1.dynupdate6.no-ip.com:8245/',
	'update': 'https://dynupdate.no-ip.com/nic/update'
}

def get_ip_addr(ver):
	try:
		r = requests.get(url[ver + '_ori'])
	except:
		r = requests.get(url[ver + '_bak'])
	return r.text

def update_ddns(username, password, hostname, ip_addr_4, ip_addr_6=''):
	params = {
		'hostname': hostname,
		'myip': ip_addr_4,
	}
	headers = {
		'user-agent': 'Individual noip-updater/' + platform.system() + '-' + platform.version() + ' chesskuo-owo@chesskuo.tw'
	}
	if ip_addr_6 != '':
		params.update({'myipv6': ip_addr_6})
	r = requests.get(
		url['update'],
		headers=headers,
		params=params,
		auth=(username, password)
	)
	res = r.text.split()
	if res[0] == 'good':
		print('[OK]', 'DNS hostname update successful.')
	elif res[0] == 'nochg':
		print('[OK]', 'IP address is current, no update performed.')
	elif res[0] == 'nohost':
		print('[ERROR]', 'Hostname supplied does not exist under specified account, client exit and require user to enter new login credentials before performing an additional request.')
	elif res[0] == 'badauth':
		print('[ERROR]', 'Invalid username password combination.')
	elif res[0] == 'badagent':
		print('[ERROR]', 'Client disabled. Client should exit and not perform any more updates without user intervention.')
	elif res[0] == '!donator':
		print('[ERROR]', 'An update request was sent, including a feature that is not available to that particular user such as offline options.')
	elif res[0] == 'abuse':
		print('[ERROR]', 'Username is blocked due to abuse.')
	elif res[0] == '911':
		print('[ERROR]', 'A fatal error on our side such as a database outage. Retry the update no sooner than 30 minutes.')

if __name__ == '__main__':
	# args parser
	parser = argparse.ArgumentParser(
		prog='noip-updater',
		usage='noip-updater [-6] -u <USERNAME> -p <PASSWORD> -H <HOSTNAME>',
	)
	parser.add_argument('-6', action='store_true', help='enable IPv6 mode')
	parser.add_argument('-u', metavar='<USERNAME>', required=True, help='your no-ip username')
	parser.add_argument('-p', metavar='<PASSWORD>', required=True, help='your no-ip password')
	parser.add_argument('-H', metavar='<HOSTNAME>', required=True, help='your no-ip ddns hostname')
	args = vars(parser.parse_args())
	# noip config
	kwargs = {
		'username': args['u'],
		'password': args['p'],
		'hostname': args['H'],
		'ip_addr_4': get_ip_addr('v4'),
		'ip_addr_6': get_ip_addr('v6') if args['6'] else '',
	}
	update_ddns(**kwargs)
