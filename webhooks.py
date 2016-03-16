from shutit_module import ShutItModule

class openshift_webhooks(ShutItModule):

	def build(self, shutit):
		shutit.send('cd /tmp/openshift_vm')
		shutit.login(command='vagrant ssh')
		shutit.login(command='sudo su -',password='vagrant',note='Become root (there is a problem logging in as admin with the vagrant user')
		shutit.send('oc login -u user2 -p anystringwilldo')                                                                                                                   
		shutit.send('oc project user2')            


		shutit.send_file('webhooks.json',r'''{
  "kind": "Template",
  "apiVersion": "v1",
  "metadata": {
    "name": "centos7-webhooks",
    "creationTimestamp": null,
    "annotations": {
      "description": "This example shows how to create and push an image with a dockerfile"
    }
  },
  "objects": [
    {
      "kind": "ImageStream",
      "apiVersion": "v1",
      "metadata": {
        "name": "centos7",
        "creationTimestamp": null
      },
      "spec": {
        "dockerImageRepository": "centos:7"
      },
      "status": {
        "dockerImageRepository": ""
      }
    },
    {
      "kind": "ImageStream",
      "apiVersion": "v1",
      "metadata": {
        "name": "myapp",
        "creationTimestamp": null
      },
      "spec": {
        "dockerImageRepository": ""
      },
      "status": {
        "dockerImageRepository": ""
      }
    },
    {
      "kind": "BuildConfig",
      "apiVersion": "v1",
      "metadata": {
        "name": "webhooks",
        "creationTimestamp": null,
        "labels": {
          "name": "webhooks-build"
        }
      },
      "spec": {
        "triggers": [{
          "type": "Generic",
          "generic": {
            "secret": "mysecret"
          }
        }],
        "source": {
          "type": "Dockerfile",
          "dockerfile": "FROM centos7:latest\nRUN yum -y install httpd"
        },
        "strategy": {
          "type": "Docker",
          "dockerStrategy": {
            "from": {
              "kind": "ImageStreamTag",
              "name": "centos7:latest"
            }
          }
        },
        "output": {
          "to": {
            "kind": "ImageStreamTag",
            "name": "myapp:latest"
          }
        },
        "postCommit": {
          "args": ["ls"]
        },
        "resources": {}
      },
      "status": {
        "lastVersion": 0
      }
    }
  ],
  "labels": {
    "template": "webhooks"
  }
}
''')
		shutit.send('oc create -f webhooks.json')
		shutit.send('oc new-app --template=centos7-webhooks')
#${CURL_COMMAND} -s -X POST -H "Authorization: bearer $TOKEN" -H "Accept: application/json" -H  "X-HTTP-Method-Override: PUT" -k ${OPENSHIFT_MASTER_URL}/oapi/v1/namespaces/${PROJECT}/buildconfigs/${AP P_NAME}/webhooks/${SECRET_WEBHOOK}/generic &> /dev/null
		shutit.send('''curl -k $(oc describe bc | grep Webhook | awk '{print $3}')''')
		shutit.logout()
		shutit.logout()
		return True

def module():
	return openshift_webhooks(
		'shutit.openshift_vm.openshift_vm.openshift_webhooks', 1418326706.008,
		description='',
		maintainer='',
		delivery_methods=['bash'],
		depends=['shutit.openshift_vm.openshift_vm.openshift_secrets']
	)

