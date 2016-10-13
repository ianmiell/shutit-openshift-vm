from shutit_module import ShutItModule

class elk(ShutItModule):

	def build(self, shutit):
		shutit.send('cd /tmp/openshift_vm')
		shutit.login(command='vagrant ssh')
		shutit.login(command='sudo su -',password='vagrant',note='Become root (there is a problem logging in as admin with the vagrant user')
		# BASIC USAGE
		shutit.send('oc login -u system:admin')
		shutit.send('oc project openshift-infra')
		shutit.send('oc secrets new logging-deployer nothing=/dev/null')
		for sc in ('logging-deployer','aggregated-logging-kibana','aggregated-logging-elasticsearch','aggregated-logging-fluentd','aggregated-logging-curator'):
			shutit.send('''oc create -f - <<API
apiVersion: v1
kind: ServiceAccount
metadata:
  name: ''' + sc + '''
secrets:
- name: ''' + sc + '''
API''')
			shutit.send('oc policy add-role-to-user edit --serviceaccount ' + sc)
			shutit.send('oadm policy add-scc-to-user privileged system:serviceaccount:logging:' + sc)
			shutit.send('oadm policy add-cluster-role-to-user cluster-reader system:serviceaccount:logging:' + sc)
			shutit.send('oadm policy add-cluster-role-to-user cluster-admin system:serviceaccount:logging:' + sc)
			shutit.send('oadm policy add-scc-to-user privileged system:serviceaccount:openshift-infra:' + sc)
			shutit.send('oadm policy add-cluster-role-to-user cluster-reader system:serviceaccount:openshift-infra:' + sc)
			shutit.send('oadm policy add-cluster-role-to-user cluster-admin system:serviceaccount:openshift-infra:' + sc)
		# Create the template
		shutit.send('curl https://raw.githubusercontent.com/openshift/openshift-ansible/e092de714dc09a86a0ff26c648eec2033a3b9952/roles/openshift_examples/files/examples/v1.1/infrastructure-templates/origin/logging-deployer.yaml | oc create -f -')
		shutit.send('oc new-app logging-deployer-template              --param KIBANA_HOSTNAME=kibana.apps.lab.com              --param ES_CLUSTER_SIZE=1              --param KIBANA_OPS_HOSTNAME=kibana-ops.apps.lab.com              --param PUBLIC_MASTER_URL=https://origin:8443')
		shutit.pause_point('pausing')
		shutit.logout()
		shutit.logout()
		return True

def module():
	return elk(
		'shutit.elk.elk.elk', 1418326706.0123124,
		description='',
		maintainer='',
		delivery_methods=['bash'],
		depends=['shutit.openshift_vm.openshift_vm.openshift_vm']
	)

