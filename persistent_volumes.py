from shutit_module import ShutItModule

class openshift_persistent_volumes(ShutItModule):

	def build(self, shutit):
		shutit.send('cd /tmp/openshift_vm')
		shutit.login(command='vagrant ssh')                                                                                                                                   
		shutit.login(command='sudo su -',password='vagrant',note='Become root (there is a problem logging in as admin with the vagrant user')        
		# PERSISTENT VOLUME SHARES
		# set up nfs share
		shutit.send('oc login -u system:admin')
		shutit.send('dnf install -y nfs-utils system-config-nfs') # https://blog.openshift.com/quick-tip-port-forwarding-and-the-all-in-one-vm/
		shutit.send('setsebool -P virt_use_nfs 1')                # allow docker to write to nfs shares(?)
		shutit.send('systemctl enable nfs-server rpcbind')
		# blat the nfs exports in existence
		shutit.send('echo > /etc/exports')
		shutit.send('oc delete pv pv01 && oc delete pv pv02 && oc delete pv pv03 && oc delete pv pv04 && oc delete pv pv05 && rm -rf /nfsvolumes')
		for num in range(1,2):
			shutit.send('mkdir -p /nfs_share_' + str(num))
			shutit.send('echo "/nfs_share_' + str(num) + '                   origin(rw,root_squash)" >> /etc/exports')
			#shutit.send('chgrp vagrant /nfs_share_' + str(num)) # doesn't work, needs to be nfsnobody
			shutit.send('chown nfsnobody: /nfs_share_' + str(num))
		shutit.send('iptables -I INPUT 1 -p tcp --dport 2049 -j ACCEPT')
		shutit.send('systemctl restart nfs-server.service')
		shutit.send('restorecon /etc/exports')
		shutit.send('systemctl restart nfs-server.service')
		shutit.send('systemctl restart rpcbind')
		# TODO: different kinds of volumes
		# create persistent volume shares
		shutit.send('oc new-project admin --description="Example project" --display-name="Hello openshift!"',note='Create a new project')
		for user in ['user1','user2','admin']:
			shutit.send_file('/tmp/nfs_' + str(user) + '.yml''','''apiVersion: "v1"
kind: "PersistentVolume"
metadata:
  name: "pv''' + str(user) + '''"
spec:
  capacity:
    storage: "5Gi"
  accessModes:
    - "ReadWriteMany"
  nfs:
    path: "/nfs_share_1"
    server: "origin"
  persistentVolumeReclaimPolicy: "Retain"''')
			shutit.send('oc create -f /tmp/nfs_' + str(user) + '.yml')
			shutit.send('oc login -u ' + str(user) + ' -p anystringwilldo',note='Log in as ' + str(user))
			shutit.send('oc project ' + str(user))
			# PERSISTENT VOLUME CLAIMS
			# claim a volume
			shutit.send_file('/tmp/pvclaim.yml','''apiVersion: "v1"
kind: "PersistentVolumeClaim"
metadata:
  name: "claim1"
spec:
  accessModes:
    - "ReadWriteMany"
  resources:
    requests:
      storage: "5Gi"''')
			shutit.send('oc create -f /tmp/pvclaim.yml')
			#shutit.send('oc get pv',note='Get our persistent volumes')
			shutit.send('oc get pvc',note='Get our persistent claims')
			shutit.send_file('/tmp/create_pod.yml','''apiVersion: "v1"
kind: "Pod"
metadata:
  name: "mypod"
  labels:
    name: "frontendhttp"
spec:
  containers:
    -
      name: "myfrontend"
      image: "nginx"
      ports:
        -
          containerPort: 80
          name: "http-server"
      volumeMounts:
        -
          mountPath: "/var/www/html"
          name: "pvol"
  volumes:
    -
      name: "pvol"
      persistentVolumeClaim:
        claimName: "claim1"''')
			shutit.send('oc create -f /tmp/create_pod.yml')
			shutit.send_until('oc get pods','.*Running.*')
			shutit.send('sleep 30 && oc exec -ti mypod touch /var/www/html/' + user)
			shutit.send('oc exec -ti mypod ls /var/www/html/')
			shutit.send('oc delete all --all')
			shutit.send('oc delete pvc claim1')
			shutit.send('oc delete pv pv' + user)
		shutit.logout()
		shutit.logout()
		return True

def module():
	return openshift_persistent_volumes(
		'shutit.openshift_vm.openshift_vm.openshift_persistent_volumes', 1418326706.010,
		description='',
		maintainer='',
		delivery_methods=['bash'],
		depends=['shutit.openshift_vm.openshift_vm.openshift_vm']
	)

