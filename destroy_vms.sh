#!/bin/bash
while true 
do
	echo DESTROYING
	VBoxManage list runningvms | grep '^"openshift-origin' | awk '{print $1}' | xargs -IXXX VBoxManage controlvm 'XXX' poweroff && VBoxManage list vms | grep '^"openshift-origin' | awk '{print $1}'  | xargs -IXXX VBoxManage unregistervm 'XXX' --delete
	if [[ $(VBoxManage list vms | grep '^"openshift-origin' | wc -l) == '0' ]]
	then
		break
	else
		ps -ef | grep virt
		ps -ef | grep virtualbox | grep '^"openshift-origin' | awk '{print $2}' | xargs kill
	fi
	echo DESTROYING
done
echo DONE
