from shutit_module import ShutItModule

class openshift_disk_abuse(ShutItModule):

	def build(self, shutit):
		shutit.send('cd /tmp/openshift_vm')
		shutit.login(command='vagrant ssh')
		shutit.login(command='sudo su -',password='vagrant',note='Become root (there is a problem logging in as admin with the vagrant user')
		# TODO: provision image and fill up disk
		shutit.send('mkdir -p tmp && cd tmp')
		shutit.send_file('Dockerfile','''FROM openshift/busybox-http-app
ENTRYPOINT cat /dev/urandom >> /tmp/afile''')
		shutit.send('oc new-app $(pwd) --strategy=docker')
		shutit.pause_point('')
		shutit.logout()
		shutit.logout()
		return True

def module():
	return openshift_disk_abuse(
		'shutit.openshift_vm.openshift_vm.openshift_disk_abuse', 1418326706.0013,
		description='Fill up the disk to see what happens to the platform.',
		maintainer='',
		delivery_methods=['bash'],
		depends=['shutit.openshift_vm.openshift_vm.openshift_vm']
	)

