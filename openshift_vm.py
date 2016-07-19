# See: https://www.openshift.org/vm/

from shutit_module import ShutItModule

class openshift_vm(ShutItModule):

	def build(self, shutit):
		shutit.send('rm -rf /tmp/openshift_vm')
		shutit.send('mkdir -p /tmp/openshift_vm')
		shutit.send('cd /tmp/openshift_vm')
		shutit.send('vagrant init thesteve0/openshift-origin')
		shutit.send('vagrant box update')
		shutit.send('vagrant up --provider virtualbox',timeout=99999)
		shutit.login(command='vagrant ssh')
		shutit.login(command='sudo su -',password='vagrant',note='Become root (there is a problem logging in as admin with the vagrant user')
		shutit.send('dnf install -y socat') # https://blog.openshift.com/quick-tip-port-forwarding-and-the-all-in-one-vm/
		# BASIC USAGE
		shutit.pause_point('')
		shutit.send('oc whoami',note='Find out who I am logged in as')
		# LOGIN, SET UP USERS
		shutit.send('oc login -u user1 -p anystringwilldo',note='Log in as user1')
		shutit.send('oc whoami -t',note='Display my login token')
		shutit.send('TOKEN=$(oc whoami -t)',note='Put token into env variable.')
		shutit.send('oc new-project user1 --description="Example project" --display-name="Hello openshift!"',note='Create a new project')
		shutit.send('oc project user1',note='Switch to that project')
		shutit.send('oc status',note='Get information about the current project')
		shutit.send('oc login -u user2 -p anystringwilldo',note='Log in as user2')
		shutit.send('oc new-project user2 --description="Example project" --display-name="Hello openshift!"',note='Create a new project')
		shutit.send('oc project user2',note='Switch to that project')
		shutit.send('oc status',note='Get information about the current project')
		shutit.logout()
		shutit.logout()
		return True

def module():
	return openshift_vm(
		'shutit.openshift_vm.openshift_vm.openshift_vm', 1418326706.00,
		description='',
		maintainer='',
		delivery_methods=['bash'],
		depends=['shutit-library.virtualbox.virtualbox.virtualbox','tk.shutit.vagrant.vagrant.vagrant']
	)

# DEBUG: oc get pod --v=10
# From: pkg/authorization/api/types.go
# oc get builds
# oc get buildconfigs
# oc get buildlogs
# oc get buildconfigs/instantiate
# oc get buildconfigs/instantiatebinary
# oc get builds/log
# oc get builds/clone
# oc get buildconfigs/webhooks
# oc get imagestreams
# oc get imagestreammappings
# oc get imagestreamtags
# oc get imagestreamimages
# oc get deployments
# oc get deploymentconfigs
# oc get generatedeploymentconfigs
# oc get deploymentconfigrollbacks
# oc get deploymentconfigs/log
# oc get deploymentconfigs/scale
# oc get clusternetworks
# oc get hostsubnets
# oc get netnamespaces
# oc get templates
# oc get templateconfigs
# oc get processedtemplates
# oc get identities
# oc get users
# oc get useridentitymappings
# oc get groups
# oc get oauthauthorizetokens
# oc get oauthaccesstokens
# oc get oauthclients
# oc get oauthclientauthorizations
# oc get policies
# oc get policybindings
# oc get roles
# oc get resourceaccessreviews" /* cluster scoped*/
# oc get subjectaccessreviews" /* cluster scoped*/
# oc get localresourceaccessreviews
# oc get localsubjectaccessreviews
# oc get routes
# oc get projects
# oc get clusterroles
# oc get clusterpolicybindings
# oc get images" /* cluster scoped*/
# oc get projectrequests
# oc get builds/details
# oc get imagestreams/status
# oc get routes/status
# oc get limitranges
# oc get resourcequotas
# oc get resourcequotausages
# oc get pods
# oc get replicationcontrollers
# oc get serviceaccounts
# oc get services
# oc get endpoints
# oc get persistentvolumeclaims
# oc get pods/log
# oc get minions
# oc get nodes
# oc get bindings
# oc get events
# oc get namespaces
# oc get persistentvolumes
# oc get securitycontextconstraints
# oc get pods/status
# oc get resourcequotas/status
# oc get namespaces/status
# oc get replicationcontrollers/status
# oc get oauthauthorizetokens
# oc get oauthaccesstokens
# oc get secrets
# oc get clusterpolicies
# oc get rolebindings DONE
# oc get clusterrolebindings DONE
