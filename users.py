from shutit_module import ShutItModule

class openshift_users(ShutItModule):

	def build(self, shutit):
		shutit.send('cd /tmp/openshift_vm')
		shutit.login(command='vagrant ssh')
		shutit.login(command='sudo su -',password='vagrant',note='Become root (there is a problem logging in as admin with the vagrant user')
		# USERS AND GROUPS
		shutit.send('oc login -u system:admin')
		shutit.send('oc describe users',note='Look up users on the system')
		shutit.send('oc describe groups',note='Look up groups on the system')
		shutit.send('oc describe policybindings',note='Describe the policy of the system (will be useful as we set up users)')
		# ROLES
		# TODO: roles etc
		# oadm policy
		# oc policy
		#shutit.send('oc get rolebinding',note='')
		#shutit.send('oc get clusterrolebinding',note='')
		shutit.logout()
		shutit.logout()
		return True

def module():
	return openshift_users(
		'shutit.openshift_vm.openshift_vm.openshift_users', 1418326706.001,
		description='',
		maintainer='',
		delivery_methods=['bash'],
		depends=['shutit.openshift_vm.openshift_vm.openshift_vm']
	)

