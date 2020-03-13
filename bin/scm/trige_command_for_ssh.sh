#!/bin/bash

this_dir=`dirname $0`
ssh_config=~/.ssh/config

if [ -f $ssh_config ]; then
	chmod -R 644 $ssh_config
fi

if [ -f $1 ]; then
        chmod -R 600 $1
fi

eval `ssh-agent -s`

private_key=$1
key_password=$2
py3_path=$3

export PATH=$py3_path:$PATH

python $this_dir/spawn.py "ssh" "${private_key}" "${key_password}"

shift
shift
$@ 

kill $SSH_AGENT_PID