from shutit_module import ShutItModule

class openshift_volumes(ShutItModule):

	def build(self, shutit):
		shutit.send('cd /tmp/openshift_vm')
		shutit.login(command='vagrant ssh')
		shutit.login(command='sudo su -',password='vagrant',note='Become root (there is a problem logging in as admin with the vagrant user')
		# VOLUMES
		# TODO: volumes
		#shutit.send('oc volume deploymentconfig --all --name myvolume -t emptyDir -m /mounteddir',note='TODO')
		#shutit.send('oc volume deploymentconfig --all --name mysecretvolume -t secret -m /mountedsecretdir --secret-name mysecret' ,note='TODO')
		#shutit.send('oc volume deploymentconfig --all --list' ,note='List all the volumes we have created')
		shutit.logout()
		shutit.logout()
		return True

def module():
	return openshift_volumes(
		'shutit.openshift_vm.openshift_vm.openshift_volumes', 1418326706.007,
		description='',
		maintainer='',
		delivery_methods=['bash'],
		depends=['shutit.openshift_vm.openshift_vm.openshift_vm']
	)

