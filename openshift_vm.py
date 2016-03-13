"""ShutIt module. See http://shutit.tk
"""

from shutit_module import ShutItModule


class openshift_vm(ShutItModule):


	def build(self, shutit):
		# Some useful API calls for reference. See shutit's docs for more info and options:
		#
		# ISSUING BASH COMMANDS
		# shutit.send(send,expect=<default>) - Send a command, wait for expect (string or compiled regexp)
		#           to be seen before continuing. By default this is managed
		#           by ShutIt with shell prompts.
		# shutit.multisend(send,send_dict)   - Send a command, dict contains {expect1:response1,expect2:response2,...}
		# shutit.send_and_get_output(send)   - Returns the output of the sent command
		# shutit.send_and_match_output(send, matches)
		#         - Returns True if any lines in output match any of
		#           the regexp strings in the matches list
		# shutit.send_until(send,regexps) - Send command over and over until one of the regexps seen in the output.
		# shutit.run_script(script)    - Run the passed-in string as a script
		# shutit.install(package)   - Install a package
		# shutit.remove(package)    - Remove a package
		# shutit.login(user='root', command='su -')
		#         - Log user in with given command, and set up prompt and expects.
		#           Use this if your env (or more specifically, prompt) changes at all,
		#           eg reboot, bash, ssh
		# shutit.logout(command='exit')   - Clean up from a login.
		#
		# COMMAND HELPER FUNCTIONS
		# shutit.add_to_bashrc(line)   - Add a line to bashrc
		# shutit.get_url(fname, locations)   - Get a file via url from locations specified in a list
		# shutit.get_ip_address()   - Returns the ip address of the target
		# shutit.command_available(command)  - Returns true if the command is available to run
		#
		# LOGGING AND DEBUG
		# shutit.log(msg,add_final_message=False) -
		#           Send a message to the log. add_final_message adds message to
		#           output at end of build
		# shutit.pause_point(msg='')   - Give control of the terminal to the user
		# shutit.step_through(msg='')  - Give control to the user and allow them to step through commands
		#
		# SENDING FILES/TEXT
		# shutit.send_file(path, contents)   - Send file to path on target with given contents as a string
		# shutit.send_host_file(path, hostfilepath)
		#         - Send file from host machine to path on the target
		# shutit.send_host_dir(path, hostfilepath)
		#         - Send directory and contents to path on the target
		# shutit.insert_text(text, fname, pattern)
		#         - Insert text into file fname after the first occurrence of
		#           regexp pattern.
		# shutit.delete_text(text, fname, pattern)
		#         - Delete text from file fname after the first occurrence of
		#           regexp pattern.
		# shutit.replace_text(text, fname, pattern)
		#         - Replace text from file fname after the first occurrence of
		#           regexp pattern.
		# ENVIRONMENT QUERYING
		# shutit.host_file_exists(filename, directory=False)
		#         - Returns True if file exists on host
		# shutit.file_exists(filename, directory=False)
		#         - Returns True if file exists on target
		# shutit.user_exists(user)     - Returns True if the user exists on the target
		# shutit.package_installed(package)  - Returns True if the package exists on the target
		# shutit.set_password(password, user='')
		#         - Set password for a given user on target
		#
		# USER INTERACTION
		# shutit.get_input(msg,default,valid[],boolean?,ispass?)
		#         - Get input from user and return output
		# shutit.fail(msg)       - Fail the program and exit with status 1
		#
		#from: https://access.redhat.com/documentation/en/openshift-enterprise/version-3.0/openshift-enterprise-30-developer-guide/
		shutit.send('rm -rf /tmp/openshift_vm')
		shutit.send('mkdir -p /tmp/openshift_vm')
		shutit.send('cd /tmp/openshift_vm')
		shutit.send('vagrant init thesteve0/openshift-origin')
		shutit.send('vagrant up --provider virtualbox')
		shutit.login(command='vagrant ssh')
		shutit.login(command='sudo su -',password='vagrant',note='Become root (there is a problem logging in as admin with the vagrant user')
		shutit.send('dnf install -y socat') # https://blog.openshift.com/quick-tip-port-forwarding-and-the-all-in-one-vm/
		# BASIC USAGE
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
