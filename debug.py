from shutit_module import ShutItModule

class openshift_debug(ShutItModule):

	def build(self, shutit):
		shutit.send('cd /tmp/openshift_vm')
		shutit.login(command='vagrant ssh')
		shutit.login(command='sudo su -',password='vagrant',note='Become root (there is a problem logging in as admin with the vagrant user')
        # debug
        shutit.send('oc get events')
		shutit.logout()
		shutit.logout()
		return True

def module():
	return openshift_debug(
		'shutit.openshift_vm.openshift_vm.openshift_debug', 1418326706.0012,
		description='',
		maintainer='',
		delivery_methods=['bash'],
		depends=['shutit.openshift_vm.openshift_vm.openshift_vm']
	)

