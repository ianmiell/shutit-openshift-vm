from shutit_module import ShutItModule

class openshift_create_app_basic(ShutItModule):

	def build(self, shutit):
		shutit.send('cd /tmp/openshift_vm')
		shutit.login(command='vagrant ssh')
		shutit.login(command='sudo su -',password='vagrant',note='Become root (there is a problem logging in as admin with the vagrant user')        
		# CREATE APP - GITHUB
		shutit.send('oc new-app https://github.com/openshift/sti-ruby.git --context-dir=2.0/test/puma-test-app',note='Create an application from a github project, specifying a directory to work from.')
		shutit.send('oc get all',note='Retrieve information about central items in this project. Our new application is there.') #description TODO
		shutit.send('oc delete all --all',note='Delete all entries, for clarity')
		# CREATE APP - GITHUB BRANCH
		shutit.send('oc new-app https://github.com/openshift/ruby-hello-world.git#beta4',note='Create an application from git repo with a branch')
		shutit.send('oc get all',note='Retrieve information about central items in this project. Our new application is there.') #description TODO
		shutit.send('oc delete all --all',note='Delete all entries, for clarity')
		# CREATE APP - GITHUB + IMAGE SPECIFIED
		shutit.send('oc new-app openshift/ruby-20-centos7:latest~https://github.com/openshift/ruby-hello-world.git',note="Use a publicly-available builder image to build a git repository's code") # TODO
		shutit.send('oc get all',note='Retrieve information about central items in this project. Our new application is there.') #description TODO
		shutit.send('oc delete all --all',note='Delete all entries, for clarity')
		# CREATE APP - DOCKER IMAGE
		shutit.send('oc new-app mysql',note='Create an application from a docker image')
		shutit.send('oc get all',note='Retrieve information about central items in this project. Our new application is there.') #description TODO
		shutit.send('oc delete all --all',note='Delete all entries, for clarity')
		# CREATE APP - DOCKER MULTI-IMAGE POD
		shutit.send('oc new-app nginx+mysql',note='Deploy nginx and mysql to the same pod')
		shutit.send('oc get all',note='Retrieve information about central items in this project. Our new application is there.') #description TODO
		shutit.send('oc delete all --all',note='Delete all entries, for clarity')
		# CREATE APP - DOCKER-MULTI-IMAGE POD + GITHUB + BUILDER IMAGE
		# TODO: ruby image is not a builder, and --strategy source doesn't work.
		#shutit.send('oc new-app ruby~https://github.com/openshift/ruby-hello-world mysql --group=ruby+mysql',note='Build a ruby image with some code, add a mysql image to the app and place them in the same pod.')
		#shutit.send('oc get all',note='Retrieve information about central items in this project. Our new application is there.') #description TODO
		shutit.logout()                                                                                                                                   
		shutit.logout()
		return True

def module():
	return openshift_create_app_basic(
		'shutit.openshift_vm.openshift_vm.openshift_create_app_basic', 1418326706.002,
		description='',
		maintainer='',
		delivery_methods=['bash'],
		depends=['shutit.openshift_vm.openshift_vm.openshift_vm']
	)

