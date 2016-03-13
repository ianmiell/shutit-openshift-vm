from shutit_module import ShutItModule

class openshift_templates(ShutItModule):

	def build(self, shutit):
		shutit.send('cd /tmp/openshift_vm')
		shutit.login(command='vagrant ssh')
		shutit.login(command='sudo su -',password='vagrant',note='Become root (there is a problem logging in as admin with the vagrant user')
		# TEMPLATES - 4.2.3 Templates
		# SIMPLE SAMPLE APP
		shutit.get_url('application-template-stibuild.json',['https://raw.githubusercontent.com/openshift/origin/master/examples/sample-app'])
		shutit.send('cat application-template-stibuild.json',note='json to create a ruby application from a template')
		shutit.send('oc create -f application-template-stibuild.json',note='Load the template into the system')
		shutit.send('oc new-app ruby-helloworld-sample',note='Create an application from this template')
		shutit.send('oc delete all --all')
		# PROCESS TEMPLATES
		shutit.send('oc process --parameters ruby-helloworld-sample',note='Show the parameters available for this template')
		shutit.send('oc new-app ruby-helloworld-sample -p ADMIN_USERNAME=jonny,ADMIN_PASSWORD=sixpack',note='Create an application from this template, passing in the template parameters to set the admin username and password.')
		shutit.send('oc delete all --all')
		shutit.logout()
		shutit.logout()
		return True

def module():
	return openshift_templates(
		'shutit.openshift_vm.openshift_vm.openshift_templates', 1418326706.004,
		description='',
		maintainer='',
		delivery_methods=['bash'],
		depends=['shutit.openshift_vm.openshift_vm.openshift_vm']
	)

