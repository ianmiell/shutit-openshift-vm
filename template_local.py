from shutit_module import ShutItModule

class openshift_template_local(ShutItModule):

	def build(self, shutit):
		shutit.send('cd /tmp/openshift_vm')
		shutit.login(command='vagrant ssh')
		shutit.login(command='sudo su -',password='vagrant',note='Become root (there is a problem logging in as admin with the vagrant user')
		# CREATE APP LOCAL - BASIC
		#shutit.send('git clone https://github.com/ianmiell/shutit-airflow',note='Get source code of project w/Dockerfile') #TODO
		#shutit.send('cd ')
		#shutit.send('oc new-app .',note='Figures out that this is a docker project and builds accordingly.')
		#shutit.send('oc get all',note='Retrieve information about central items in this project. Our new application is there.') #description TODO
		#shutit.send('oc delete all --all',note='Delete all entries, for clarity')

		# CREATE APP - DOCKERFILE LOCAL SOURCE
		shutit.send_file('application-template-dockerfile.json',r'''{
  "kind": "Template",
  "apiVersion": "v1",
  "metadata": {
    "name": "centos7-dockerfile-local",
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
        "name": "dockerfile-local",
        "creationTimestamp": null,
        "labels": {
          "name": "dockerfile-local-build"
        }
      },
      "spec": {
        "triggers": [],
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
    "template": "application-template-dockerbuild"
  }
}
''')
		shutit.send('oc create -f application-template-dockerfile.json')
		shutit.send('oc new-app --template=centos7-dockerfile-local')
		shutit.send('oc get all')
		# CREATE APP - DOCKER BINARY SOURCE - TODO
		shutit.logout()
		shutit.logout()
		return True

def module():
	return openshift_template_local(
		'shutit.openshift_vm.openshift_vm.openshift_template_local', 1418326706.003,
		description='',
		maintainer='',
		delivery_methods=['bash'],
		depends=['shutit.openshift_vm.openshift_vm.openshift_vm']
	)

