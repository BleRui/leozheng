#!/usr/bin/python
# -*- coding: utf-8 -*-

import os,sys,util
import base64

def scm_ssh_access(stream_info):
    trige_ssh_command = ''
    private_key="/tmp/."+stream_info['STREAM_NAME']+'_'+stream_info['TOOL_TYPE']+"_private_key"
    key_password = ""
    current_path=sys.path[0]
    host = ''
    if "HOST" in stream_info and stream_info["HOST"] != "":
        host = stream_info["HOST"]
    if not os.path.exists(os.environ['HOME']+"/.ssh"):
        os.makedirs(os.environ['HOME']+"/.ssh")
    ssh_config_file = os.environ['HOME']+"/.ssh/config"

    if not os.path.exists(ssh_config_file):
        print("create ssh config: "+ssh_config_file)
        os.mknod(ssh_config_file) 
        
    if host != "":
        add_status = False
        with open(ssh_config_file, 'r') as ssh_config:
                lines = ssh_config.readlines()
                for line in lines:
                        if host in line:
                                add_status = True
        if not add_status:
                with open(ssh_config_file, 'a+') as ssh_config:
                        ssh_config.write("\n")
                        ssh_config.write("Host "+host+"\n")
                        ssh_config.write("HostName "+host+"\n")
                        ssh_config.write("Port 22\n")
                        ssh_config.write("\n")
    if not "SSH_PRIVATE_KEY_SAVE" in stream_info:
        if os.path.isfile(private_key):
            os.remove(private_key)
        with open(private_key, 'w') as key_file:
            key_content = base64.b64decode(stream_info['SSH_PRIVATE_KEY']).decode("utf-8") 
            key_file.write(key_content)
    if "PASSWORD" in stream_info:
        #key_password = base64.b64decode(stream_info['PASSWORD']).decode("utf-8") 
        key_password = stream_info['PASSWORD']
    if os.path.isfile(private_key): 
        os.system('chmod -R 755 '+current_path+'/scm/trige_command_for_ssh.sh ')
        trige_ssh_command = current_path+"/scm/trige_command_for_ssh.sh "+private_key+" \'"+key_password+"\' "+stream_info['PY35_PATH']
    return trige_ssh_command
    