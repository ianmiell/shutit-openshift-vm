from shutit_module import ShutItModule

class openshift_extras(ShutItModule):

	def build(self, shutit):
		shutit.send('cd /tmp/openshift_vm')
		shutit.login(command='vagrant ssh')
		shutit.login(command='sudo su -',password='vagrant',note='Become root (there is a problem logging in as admin with the vagrant user')
		# EXTRAS
		shutit.send('openshift ex diagnostics',check_exit=False)
		shutit.logout()
		shutit.logout()
		return True

def module():
	return openshift_extras(
		'shutit.openshift_vm.openshift_vm.openshift_extras', 1418326706.0099,
		description='',
		maintainer='',
		delivery_methods=['bash'],
		depends=['shutit.openshift_vm.openshift_vm.openshift_vm']
	)

