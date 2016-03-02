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
		shutit.login(command='sudo su -',note='Become root (there is a problem logging in as admin with the vagrant user')
		shutit.send('yum install -y socat') # https://blog.openshift.com/quick-tip-port-forwarding-and-the-all-in-one-vm/
		# PERSISTENT VOLUME SHARES
		# set up nfs share
		shutit.send('yum install -y nfs-utils system-config-nfs') # https://blog.openshift.com/quick-tip-port-forwarding-and-the-all-in-one-vm/
		shutit.send('systemctl enable rpcbind nfs-server')
		shutit.send('systemctl start rcpbind')
		shutit.send('systemctl start nfs-server')
		shutit.send('mkdir -p /nfs_share')
		shutit.send('echo "/nfs_share                   localhost.localdomain(rw,root_squash)" >> /etc/exports')
		shutit.send('iptables -I INPUT 1 -p tcp --dport 2049 -j ACCEPT')
		shutit.send('systemctl restart nfs-server.service')
		shutit.send('restorecon /etc/exports')
		shutit.send('systemctl restart nfs-server.service')
		# client nfs
		shutit.send('mkdir -p /media/nfs')
		shutit.send('mount localhost.localdomain:/nfs_share /media/nfs')
		# create persistent volume shares
		for num in range(1,11):
			shutit.send_file('''/tmp/nfs.json''','''apiVersion: "v1"
kind: "PersistentVolume"
metadata:
  name: "pv000''' + str(num) + '''" 
spec:
  capacity:
    storage: "5Gi" 
  accessModes:
    - "ReadWriteMany" 
  nfs: 
    path: "/nfs_share" 
    server: "localhost" 
  persistentVolumeReclaimPolicy: "Recycle"''')
			shutit.send('oc create -f /tmp/nfs.json && rm -f /tmp/nfs.json')
		# BASIC USAGE
		shutit.send('oc whoami',note='Find out who I am logged in as')
		# USERS AND GROUPS
		shutit.send('oc describe users',note='Look up users on the system')
		shutit.send('oc describe groups',note='Look up groups on the system')
		shutit.send('oc describe policybindings',note='Describe the policy of the system (will be useful as we set up users)')
		# LOGIN
		shutit.send('oc login -u admin -p anystringwilldo',note='Log in as admin')
		shutit.send('oc whoami -t',note='Display my login token')
		shutit.send('TOKEN=$(oc whoami -t)',note='Put token into env variable.')
		# CREATE PROJECT - BASIC
		shutit.send('oc new-project hello-openshift --description="Example project" --display-name="Hello openshift!"',note='Create a new project')
		shutit.send('oc project new-project',note='Switch to that project')
		shutit.send('oc status',note='Get information about the current project')
		#shutit.send('git clone https://github.com/ianmiell/shutit-airflow',note='Get source code of project w/Dockerfile') #TODO
		#shutit.send('cd ') 
		#shutit.send('oc new-app .',note='Figures out that this is a docker project and builds accordingly.')
		#shutit.send('oc get all',note='Retrieve information about central items in this project. Our new application is there.') #description TODO
		#shutit.send('oc delete all --all',note='Delete all entries, for clarity')
		# CREATE PROJECT - GITHUB
		shutit.send('oc new-app https://github.com/openshift/sti-ruby.git --context-dir=2.0/test/puma-test-app',note='Create an application from a github project, specifying a directory to work from.')
		shutit.send('oc get all',note='Retrieve information about central items in this project. Our new application is there.') #description TODO
		shutit.send('oc delete all --all',note='Delete all entries, for clarity')
		# CREATE PROJECT - GITHUB BRANCH
		shutit.send('oc new-app https://github.com/openshift/ruby-hello-world.git#beta4',note='Create an application from git repo with a branch')
		shutit.send('oc get all',note='Retrieve information about central items in this project. Our new application is there.') #description TODO
		shutit.send('oc delete all --all',note='Delete all entries, for clarity')
		# CREATE PROJECT - GITHUB + IMAGE SPECIFIED
		shutit.send('oc new-app openshift/ruby-20-centos7:latest~https://github.com/openshift/ruby-hello-world.git',note="Use a publicly-available builder image to build a git repository's code") # TODO
		shutit.send('oc get all',note='Retrieve information about central items in this project. Our new application is there.') #description TODO
		shutit.send('oc delete all --all',note='Delete all entries, for clarity')
		# CREATE PROJECT - DOCKER IMAGE
		shutit.send('oc new-app mysql',note='Create an application from a docker image')
		shutit.send('oc get all',note='Retrieve information about central items in this project. Our new application is there.') #description TODO
		shutit.send('oc delete all --all',note='Delete all entries, for clarity')
		# CREATE PROJECT - DOCKER MULTI-IMAGE POD
		shutit.send('oc new-app nginx+mysql',note='Deploy nginx and mysql to the same pod')
		shutit.send('oc get all',note='Retrieve information about central items in this project. Our new application is there.') #description TODO
		shutit.send('oc delete all --all',note='Delete all entries, for clarity')
		# CREATE PROJECT - DOCKER-MULTI-IMAGE POD + GITHUB + BUILDER IMAGE
		shutit.send('oc new-app ruby~https://github.com/openshift/ruby-hello-world mysql --group=ruby+mysql',note='Build a ruby image with some code, add a mysql image to the app and place them in the same pod.')
		shutit.send('oc get all',note='Retrieve information about central items in this project. Our new application is there.') #description TODO
		shutit.send('oc delete all --all',note='Delete all entries, for clarity')

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

		# IMAGE STREAM
		shutit.send_file('/tmp/imagestream.json','''
  {
      "kind": "ImageStream",
      "apiVersion": "v1",
      "metadata": {
        "name": "airflow"
      },
      "spec": {},
      "status": {
        "dockerImageRepository": ""
      }
  }''')
		shutit.send('oc create -f /tmp/imagestream.json')
		# BUILD CONFIG
		shutit.send_file('/tmp/buildconfig.json','''
  {
      "kind": "BuildConfig",
      "apiVersion": "v1",
      "metadata": {
        "name": "airflow",
        "labels": {
          "name": "airflow-build"
        }
      },
      "spec": {
        "triggers": [
          {
            "type": "GitHub",
            "github": {
              "secret": "secret101"
            }
          },
          {
            "type": "Generic",
            "generic": {
              "secret": "secret101"
            }
          }
        ],
        "source": {
          "type": "Git",
          "git": {
            "uri": "https://github.com/ianmiell/shutit-airflow"
          }
        },
        "strategy": {
          "type": "Docker"
        },
        "output": {
          "to": {
            "kind": "ImageStreamTag",
            "name": "airflow:latest"
          }
        }
      }
    }
''')
		shutit.send('oc create -f /tmp/buildconfig.json')
		# AIRFLOW BUILD
		shutit.send('oc describe buldconfig airflow',note='Ideally you would take this github url, and update your github webhooks for this project. But there is no public URL for this server so we will skip and trigger a build manually.')
		shutit.send('oc start-build airflow',note='Trigger a build by hand')
		shutit.send('oc build-logs airflow-1',note='Follow the build and wait for it to terminate')

		# DEPLOYMENT CONFIG
		shutit.send_file('/tmp/deploymentconfig.json','''
    {
      "kind": "DeploymentConfig",
      "apiVersion": "v1",
      "metadata": {
        "name": "airflow"
      },
      "spec": {
        "strategy": {
          "type": "Rolling",
          "rollingParams": {
            "updatePeriodSeconds": 1,
            "intervalSeconds": 1,
            "timeoutSeconds": 120
          },
          "resources": {}
        },
        "triggers": [
          {
            "type": "ImageChange",
            "imageChangeParams": {
              "automatic": true,
              "containerNames": [
                "nodejs-helloworld"
              ],
              "from": {
                "kind": "ImageStreamTag",
                "name": "airflow:latest"
              }
            }
          },
          {
            "type": "ConfigChange"
          }
        ],
        "replicas": 1,
        "selector": {
          "name":"airflow"
          },
        "template": {
          "metadata": {
            "labels": {
              "name": "airflow"
            }
          },
          "spec": {
            "containers": [
              {
                "name": "airflow",
                "image": "airflow",
                "ports": [
                  {
                    "containerPort": 8080,
                    "protocol": "TCP"
                  }
                ],
                "resources": {},
                "terminationMessagePath": "/dev/termination-log",
                "imagePullPolicy": "IfNotPresent",
                "securityContext": {
                  "capabilities": {},
                  "privileged": false
                }
              }
            ],
            "restartPolicy": "Always",
            "dnsPolicy": "ClusterFirst"
          }
        }
      },
      "status": {}
    }
''')
		shutit.send('oc create -f /tmp/deploymentconfig.json')

		# Chapter 11 image pull secrets

		# SECRETS
		# Chapter 10 Secrets
		shutit.send('''cat > username << END
mysecretusername
END''',note='create a secret username file')
		shutit.send('''cat > password << END
mysecretpassword
END''',note='create a secret password file')
		shutit.send('''cat > docker.cfg << END
my
secret
cfg
file
END''',note='create a secret docker.cfg')
		shutit.send('''cat > secret.json << END
{
  "apiversion": "v1",
  "kind": "secret",
  "name": "mysecret",
  "namespace": "hello-openshift",
  "data": {
 "username": "$(base64 username)",
 "password": "$(base64 password)"
  }
}
END''')
		shutit.send('oc create -f secret.json',note='create the secret from the json file')
		# TODO: use the secret
		
		# TODO: cf Examples link in 10.3.2 / 10.5

		# VOLUMES
		# TODO: volumes
		shutit.send('oc volume deploymentconfig --all --name myvolume -t emptyDir -m /mounteddir',note='TODO')
		shutit.send('oc volume deploymentconfig --all --name mysecretvolume -t secret -m /mountedsecretdir --secret-name mysecret' ,note='TODO')
		shutit.send('oc volume deploymentconfig --all --list' ,note='List all the volumes we have created')

		# ROLES
		# TODO: roles etc
		# oadm policy
		# oc policy
		#shutit.send('oc get rolebinding',note='')
		#shutit.send('oc get clusterrolebinding',note='')

		# PERSISTENT VOLUME CLAIMS
		# claim a volume
		shutit.send_file('/tmp/pvclaim.json','''apiVersion: "v1"
kind: "PersistentVolumeClaim"
metadata:
  name: "claim1"
spec:
  accessModes:
    - "ReadWriteMany"
  resources:
    requests:
      storage: "5Gi"''')
		shutit.send('oc create -f /tmp/pvclaim.json && rm -f /tmp/pvclaim.json')
		shutit.send('oc get pvc',note='Get our persistent claims')
		shutit.send('oc get pv',note='Get our persistent volumes')
			
		# EXTRAS	
		shutit.send('openshift ex diagnostics')
		shutit.pause_point('')
		shutit.logout()
		shutit.logout()
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
		return True

	def get_config(self, shutit):
		# CONFIGURATION
		# shutit.get_config(module_id,option,default=None,boolean=False)
		#         - Get configuration value, boolean indicates whether the item is
		#           a boolean type, eg get the config with:
		# shutit.get_config(self.module_id, 'myconfig', default='a value')
		#           and reference in your code with:
		# shutit.cfg[self.module_id]['myconfig']
		return True

	def test(self, shutit):
		# For test cycle part of the ShutIt build.
		return True

	def finalize(self, shutit):
		# Any cleanup required at the end.
		return True
	
	def is_installed(self, shutit):
		return False


def module():
	return openshift_vm(
		'shutit.openshift_vm.openshift_vm.openshift_vm', 1418326706.00,
		description='',
		maintainer='',
		delivery_methods=['bash'],
		depends=['shutit-library.virtualbox.virtualbox.virtualbox','tk.shutit.vagrant.vagrant.vagrant']
	)

