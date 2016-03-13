from shutit_module import ShutItModule

class openshift_airflow(ShutItModule):

	def build(self, shutit):
		shutit.send('cd /tmp/openshift_vm')
		shutit.login(command='vagrant ssh')
		shutit.login(command='sudo su -',password='vagrant',note='Become root (there is a problem logging in as admin with the vagrant user')
		# AIRFLOW BUILD
		# Takes too long.
		#shutit.send('oc describe buildconfig airflow',note='Ideally you would take this github url, and update your github webhooks for this project. But there is no public URL for this server so we will skip and trigger a build manually.')
		#shutit.send('oc start-build airflow',note='Trigger a build by hand')
		#shutit.send('sleep 60 && oc logs -f build/airflow-1',note='Follow the build and wait for it to terminate')

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
		shutit.logout()
		shutit.logout()
		return True

def module():
	return openshift_airflow(
		'shutit.openshift_vm.openshift_vm.openshift_airflow', 1418326706.005,
		description='',
		maintainer='',
		delivery_methods=['bash'],
		depends=['shutit.openshift_vm.openshift_vm.openshift_vm']
	)

