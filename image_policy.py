from shutit_module import ShutItModule

class openshift_image_policy(ShutItModule):

	def build(self, shutit):
		shutit.send('cd /tmp/openshift_vm')
		shutit.login(command='vagrant ssh')
		shutit.login(command='sudo su -',password='vagrant',note='Become root (there is a problem logging in as admin with the vagrant user')
#Get the digest from oc get istag/image-policy-check:latest and use it for oc annotate images/<digest> images.openshift.io/deny-execution=true. For example:
#$ oc annotate images/sha256:09ce3d8b5b63595ffca6636c7daefb1a615a7c0e3f8ea68e5db044a9340d6ba8 images.openshift.io/deny-execution=true
		shutit.logout()
		shutit.logout()
		return True

def module():
	return openshift_image_policy(
		'shutit.openshift_vm.openshift_vm.openshift_image_policy', 1418326706.0015,
		description='Demonstrate image policy enforcement on an internal image.',
		maintainer='',
		delivery_methods=['bash'],
		depends=['shutit.openshift_vm.openshift_vm.openshift_vm']
	)

