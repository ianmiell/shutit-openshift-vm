from shutit_module import ShutItModule

import base64

class openshift_secrets(ShutItModule):

	def build(self, shutit):
		shutit.send('cd /tmp/openshift_vm')
		shutit.login(command='vagrant ssh')
		shutit.login(command='sudo su -',password='vagrant',note='Become root (there is a problem logging in as admin with the vagrant user')
		shutit.send('oc login -u user2 -p anystringwilldo')
		shutit.send('oc project user2')

		# Chapter 11 image pull secrets
		# SECRETS
		# Chapter 10 Secrets
		# TODO
		shutit.send_file('secret.json','''{
  "apiVersion": "v1",
  "kind": "Secret",
  "metadata": {
    "name": "mysecret-secrets"
  },
  "namespace": "user2",
  "data": { 
    "username": "''' + base64.b64encode('myusername') + '''"
  }
}''')
		shutit.send('oc create -f secret.json')

		shutit.send('''cat > docker.cfg << END
{
	"https://index.docker.io/v1/": {
		"auth": "W1pIWxdOaRoXYp6YXJka",
		"email": "ian.miell@gmail.com"
	}
}
END''',note='create a secret docker.cfg')
		# TODO use these
		shutit.logout()
		shutit.logout()
		return True

def module():
	return openshift_secrets(
		'shutit.openshift_vm.openshift_vm.openshift_secrets', 1418326706.006,
		description='',
		maintainer='',
		delivery_methods=['bash'],
		depends=['shutit.openshift_vm.openshift_vm.openshift_vm']
	)

