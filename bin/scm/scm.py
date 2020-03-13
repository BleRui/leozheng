#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys,os,subprocess
import file,util,ssh
import xml.etree.ElementTree as ET
import datetime
import re
import pid_config
import multiprocessing
import urllib.parse
import linecache
import result
import time
import platform
import urllib.request
import json

current_path=sys.path[0]


def print_revision_latest_time(stream_info):
    latest_info = ''
    stream_code_path = ''
    try:
        if 'REPO_RELPATH_MAP' in stream_info and json.loads(stream_info['REPO_RELPATH_MAP']) != {}:
            repo_relpath_map = json.loads(stream_info['REPO_RELPATH_MAP'])
            for key in repo_relpath_map.keys():
                temp_path = ''.join(stream_info["STREAM_CODE_PATH"]+'/'+repo_relpath_map[key].replace('./', '/')).replace('//', '/')
                latest_info += revision_latest_time(stream_info, temp_path)
        else:
            latest_info += revision_latest_time(stream_info, stream_info['STREAM_CODE_PATH'])
    except Exception as e:
        raise Exception(e)
    return latest_info

def revision_latest_time(stream_info, stream_code_path):
    command = ""
    latest_info = ""
    user_name = '提交人'
    revision = '版本号'
    latest_time = '提交时间'
    try:
        if stream_info["SCM_TYPE"] == "svn":
            command = ' svn info --xml '+stream_code_path
        elif stream_info["SCM_TYPE"] == "git":
            if not os.path.exists(stream_code_path):
                return latest_info
            os.chdir(stream_code_path)
            command = "git log --pretty=format:\"%an->%h->%ad\" --date=iso -1"
        
        p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,shell=True)
        if stream_info["SCM_TYPE"] == "svn":
            message = ''
            file_svn_info_xml = stream_code_path+'/file_svn_info.xml'
            for line in p.stdout:
                message += line.decode().strip() +'\n'
            if "url" in message:
                with open(file_svn_info_xml, 'w') as file:
                    file.write(message)
                if os.path.isfile(file_svn_info_xml):
                    tree = ET.ElementTree(file=file_svn_info_xml)
                    for elem in tree.iter():
                        if "commit" == elem.tag:
                            revision += elem.attrib['revision']
                        elif "author" == elem.tag:
                            user_name += elem.text
                        elif "date" == elem.tag:
                            latest_time += elem.text
            latest_info = revision+'，'+latest_time+'，'+user_name
            if os.path.exists(file_svn_info_xml):
                os.remove(file_svn_info_xml)
        elif stream_info["SCM_TYPE"] == "git":
            for line in p.stdout:
                line = line.decode().strip()
                if "->" in line:
                    msg_array = line.split('->')
                    if len(msg_array) == 3:
                        user_name += msg_array[0]
                        revision += msg_array[1]
                        latest_time += msg_array[2]
            latest_info = revision+'，'+latest_time+'，'+user_name
            os.chdir(current_path)
    except Exception as e:
        raise Exception(e)
    return latest_info+'\n'

def get_modules(stream_code_path):
    gitmodules = stream_code_path+'/.gitmodules'
    module_info = {}
    module_list = []
    try:
        if os.path.exists(gitmodules):
            with open(gitmodules, 'r', encoding = 'utf-8') as gitmodules_file:
                for line in gitmodules_file.readlines():
                    if '[submodule' in line and module_info:
                        module_list.append(module_info)
                        module_info = {}
                    if not '[submodule' in line:
                        if '=' in line and 'path' in line:
                            module_info['path'] = line.strip().split('=')[1].replace(' ','')
                        if '=' in line and 'url' in line:
                            module_info['url'] = line.strip().split('=')[1].replace(' ','')
                        if '=' in line and 'branch' in line:
                            module_info['branch'] = line.strip().split('=')[1]
                if module_info:
                    module_list.append(module_info)
    except Exception as e:
        raise Exception(e)
        
    return  module_list
        
def get_stream_code_path(stream_info, file_path):
    stream_code_path = ''
    try:
        if 'REPO_RELPATH_MAP' in stream_info and json.loads(stream_info['REPO_RELPATH_MAP']) != {}:
            repo_relpath_map = json.loads(stream_info['REPO_RELPATH_MAP'])
            for key in repo_relpath_map.keys():
                temp_path = ''.join(stream_info["STREAM_CODE_PATH"]+'/'+repo_relpath_map[key].replace('./', '/')).replace('//', '/')
                if temp_path in file_path:
                    stream_code_path = temp_path
                    break
        else:
            stream_code_path=stream_info['STREAM_CODE_PATH']
    except Exception as e:
        raise Exception(e)
    return stream_code_path
    
def generate_blame_and_info(stream_info):
    try:
        project_file_list=stream_info['PROJECT_FILE_LIST']
        if stream_info["SCM_TYPE"] == "svn" and stream_info["CERT_TYPE"] == "ssh" and not 'OFFLINE' in stream_info:
            stream_info["SSH_PRIVATE_KEY_SAVE"] = True
            
        if os.path.isfile(project_file_list):
            with open(project_file_list, "r", encoding = 'utf-8') as file:
                process_blame = multiprocessing.Pool(processes = int(stream_info['POOL_PROCESSES']))
                blame_count=0
                for file_path in file.readlines():
                    file_path=file_path.strip().replace('//','/')
                    if os.path.isfile(file_path):
                        try:
                            stream_code_path = get_stream_code_path(stream_info, file_path)
                            blame_count+=1
                            process_blame.apply_async(blame_run, (file_path,stream_info,stream_code_path, ))
                        except Exception as e:
                                print(e)
                #print(util.get_datetime()+" blame file count:"+str(blame_count))
                process_blame.close()
                process_blame.join() 
        if "SSH_PRIVATE_KEY_SAVE" in stream_info:
            del stream_info["SSH_PRIVATE_KEY_SAVE"]
            private_key="/tmp/."+stream_info['STREAM_NAME']+'_'+stream_info['TOOL_TYPE']+"_private_key"
            if os.path.exists(private_key):
                os.remove(private_key)
        os.chdir(current_path)
    except Exception as e:
        raise Exception(e)

def blame_run(file_path, stream_info, stream_code_path):
    try:
        filename_result=result.get_result_file_path(stream_info["STREAM_RESULT_PATH"],file_path)
        file_path_url=filename_result+".scm_url.xml"
        file_path_info=filename_result+".scm_info.xml"
        file_path_blame=filename_result+".scm_blame.xml"
        txt_file_path_blame=filename_result+".scm_blame.txt"
        #print(util.get_datetime()+" get "+stream_info["SCM_TYPE"]+" "+stream_info["CERT_TYPE"]+" scm info "+file_path)
        #print(util.get_datetime()+" get "+stream_info["SCM_TYPE"]+" "+stream_info["CERT_TYPE"]+" scm blame "+file_path)
        scm_info_command = ""
        scm_blame_command = ""
        scm_url_command = ""
        
        if stream_info["SCM_TYPE"] == "svn" and stream_info["CERT_TYPE"] == "http":
            scm_url_command = "svn info --non-interactive  --no-auth-cache --trust-server-cert --username "+stream_info["ACCOUNT"]+" --password "+stream_info["PASSWORD"]+" --xml \""+file_path+"\" >\""+file_path_url+"\""
            scm_info_command = "svn log -r 1:HEAD --limit 1 --xml --non-interactive  --no-auth-cache --trust-server-cert --username "+stream_info["ACCOUNT"]+" --password "+stream_info["PASSWORD"]+" \""+file_path+"\" >\""+file_path_info+"\""
            scm_blame_command = "svn blame --non-interactive  --no-auth-cache --trust-server-cert --username "+stream_info["ACCOUNT"]+" --password "+stream_info["PASSWORD"]+" --xml \""+file_path+"\" >\""+file_path_blame+"\""
        elif stream_info["SCM_TYPE"] == "svn" and stream_info["CERT_TYPE"] == "ssh" and not 'OFFLINE' in stream_info:
            ssh_access_command = ssh.scm_ssh_access(stream_info)
            scm_url_command = " svn info  --xml \""+file_path+"\" >\""+file_path_url+"\""
            scm_info_command = ssh_access_command+" svn log -r 1:HEAD --limit 1 --xml \""+file_path+"\" | grep -v ^$ | grep -v \'Agent pid\' >\""+file_path_info+"\""
            scm_blame_command = ssh_access_command+" svn blame  --xml \""+file_path+"\" | grep -v ^$ | grep -v \'Agent pid\' | grep -v \'spawn ssh-add\' | grep -v \'Enter passphrase for\' | grep -v \'Identity added:\' >\""+file_path_blame+"\""
        elif stream_info["SCM_TYPE"] == "svn" and stream_info["CERT_TYPE"] == "ssh" and 'OFFLINE' in stream_info:
            scm_url_command = " svn info  --xml \""+file_path+"\" >\""+file_path_url+"\""
            scm_info_command = " svn log -r 1:HEAD --limit 1 --xml \""+file_path+"\" >\""+file_path_info+"\""
            scm_blame_command = " svn blame  --xml \""+file_path+"\" >\""+file_path_blame+"\""
        elif stream_info["SCM_TYPE"] == "git":
            module_list = get_modules(stream_code_path)
            for info in module_list:
                    sub_path = ''.join(stream_code_path+'/'+info['path']).replace('//','/')
                    if sub_path in file_path:
                        #print('match :'+str(file_path))
                        os.chdir(sub_path)
                        break
            else:
                os.chdir(stream_code_path)
            scm_url_command = "git log --pretty=format:%h \""+file_path+"\" >\""+file_path_url+"\""
            scm_info_command = "git log --pretty=format:\"%ad\" --date=iso --reverse \""+file_path+"\" >\""+file_path_info+"\""
            scm_blame_command = "git blame \""+file_path+"\" -t >\""+file_path_blame+"\""
        elif stream_info["SCM_TYPE"] == "http_download":
            scm_url_command = 'echo >\"'+file_path_url+'\"'
            scm_info_command = 'echo >\"'+file_path_info+'\"'
            scm_blame_command = 'echo >\"'+file_path_blame+'\"'
            os.system('echo >\"'+txt_file_path_blame+'\"')
        os.system(scm_info_command + ' 2>/dev/null')
        os.system(scm_blame_command + ' 2>/dev/null')
        os.system(scm_url_command + ' 2>/dev/null')
        check_rerun = False
        if stream_info["SCM_TYPE"] != 'http_download':
            if os.path.isfile(file_path_blame):
                try:
                    with open(file_path_blame, "rb") as file:
                        allens = len(file.readlines())
                        if allens < 3:
                            check_rerun = True
                except Exception as e:
                    print("=>scm.py->blame_run->ERROR:"+str(e)+file_path_blame)
            #if check_rerun:
            #    #print(util.get_datetime()+" scm blame failed again try: "+file_path_blame)
            #    os.system(scm_blame_command)
            translate_blame_xml(file_path_blame, txt_file_path_blame, stream_info)
    except Exception as e:
        raise Exception(e)
        
def translate_blame_xml(file_path_blame, txt_file_path_blame, stream_info):
    try:
        if os.path.isfile(file_path_blame):
            if stream_info["SCM_TYPE"] == "svn":
                tree = ET.ElementTree(file=file_path_blame)
                with open(txt_file_path_blame, "w", encoding = 'utf-8') as file:
                    for elem in tree.iter():
                        if "entry" == elem.tag:
                            line_info = elem.attrib['line-number']
                            for subelem in elem.iter():
                                if "author" == subelem.tag:
                                    line_info = line_info +"->"+subelem.text
                                if "date" == subelem.tag:
                                    line_info = line_info +"->"+subelem.text
                            file.write(line_info+"\n")
            elif stream_info["SCM_TYPE"] == "git":
                with open(txt_file_path_blame, "w", encoding = 'utf-8') as file:
                    try:
                        with open(file_path_blame, "r", encoding='utf-8') as blame_file:
                            lines = blame_file.readlines()
                            for line in lines:
                                line = ' '.join(line.replace('-', '+').replace(' +', '+').split())
                                line = line[line.index('('):]
                                line_arrary = line.split(' ')
                                if len(line_arrary) >= 3:
                                    author = line_arrary[0][1:]
                                    num_line = ''
                                    change_time = ''
                                    if "(" in author:
                                        author = author.split('(')[0]
                                    if not '+' in line_arrary[1]:
                                        author += line_arrary[1]
                                        if len(line_arrary) < 4:
                                            continue
                                        num_line = line_arrary[3][:-1]
                                        change_time = datetime.datetime.fromtimestamp(int(line_arrary[2].split('+')[0])).strftime('%Y-%m-%dT%H:%M:%S.%f%z')
                                    else:
                                        num_line = line_arrary[2][:-1]
                                        change_time = datetime.datetime.fromtimestamp(int(line_arrary[1].split('+')[0])).strftime('%Y-%m-%dT%H:%M:%S.%f%z')
                                    line_info = num_line + '->'+author+'->'+change_time
                                    file.write(line_info+"\n")
                    except:
                        with open(file_path_blame, "rb") as blame_file:
                            lines = blame_file.readlines()
                            for line in lines:
                                line = str(line)
                                line = ' '.join(line.replace('-', '+').replace(' +', '+').split())
                                line = line[line.index('('):]
                                line_arrary = line.split(' ')
                                if len(line_arrary) >= 3:
                                    author = line_arrary[0][1:]
                                    num_line = ''
                                    change_time = ''
                                    if "(" in author:
                                        author = author.split('(')[0]
                                    if not '+' in line_arrary[1]:
                                        author += line_arrary[1]
                                        if len(line_arrary) < 4:
                                            continue
                                        num_line = line_arrary[3][:-1]
                                        change_time = datetime.datetime.fromtimestamp(int(line_arrary[2].split('+')[0])).strftime('%Y-%m-%dT%H:%M:%S.%f%z')
                                    else:
                                        num_line = line_arrary[2][:-1]
                                        change_time = datetime.datetime.fromtimestamp(int(line_arrary[1].split('+')[0])).strftime('%Y-%m-%dT%H:%M:%S.%f%z')
                                    line_info = num_line + '->'+author+'->'+change_time
                                    file.write(line_info+"\n")
    except Exception as e:
        raise Exception(e)
        
def parse_info_xml(info_xml_file, stream_info):
    file_change_time=""
    try:
        if os.path.isfile(info_xml_file):
            if stream_info["SCM_TYPE"] == "svn":
                if os.path.getsize(info_xml_file):
                    tree = ET.ElementTree(file=info_xml_file)
                    for elem in tree.iter():
                        if "date" == elem.tag:
                            file_change_time=elem.text
                st = time.strptime(file_change_time, '%Y-%m-%dT%H:%M:%S.%fZ')
                file_change_time = int(round(time.mktime(st) * 1000))
            elif stream_info["SCM_TYPE"] == "git":
                file_change_time = linecache.getline(info_xml_file,1).strip()
                st = time.strptime(file_change_time, '%Y-%m-%d %H:%M:%S %z')
                file_change_time = int(round(time.mktime(st) * 1000))
            elif stream_info["SCM_TYPE"] == "http_download":
                file_change_time = datetime.datetime.fromtimestamp(int(time.time())).strftime('%Y-%m-%dT%H:%M:%S.%f%z')
            # if file_change_time == ""
            # st = time.strptime(file_change_time, '%Y-%m-%d %H:%M:%S %z')
            # file_change_time = int(round(time.mktime(st) * 1000))
    except Exception as e:
        raise Exception(e)
        pass
    return file_change_time
    
def parse_log_xml(log_xml_file, file_path, stream_info):
    file_scm_info = {}
    file_scm_info['sub_module']=''
    try:
        stream_code_path = get_stream_code_path(stream_info, file_path)
        module_list = get_modules(stream_code_path)
        file_scm_info['rel_path'] = file_path.replace(stream_code_path, '').replace('\\','/').replace('//','/')
        if file_scm_info['rel_path'].startswith('/'):
            file_scm_info['rel_path'] = file_scm_info['rel_path'][1:]
        for info in module_list:
            if info['path'].startswith('/'):
                info['path'] = info['path'][1:]
            if re.search('^'+info['path']+'*', file_scm_info['rel_path']):
                if 'http://' in info['url'] or 'https://' in info['url']:
                    temp_data = info['url'].replace('.git', '').replace('//', '')
                    file_scm_info['sub_module'] = temp_data.split('/', 1)[1]
                elif 'git@' in info['url']:
                    temp_data = info['url'].replace('.git', '')
                    file_scm_info['sub_module'] = temp_data.split(':', 1)[1]
                file_scm_info['rel_path'] = file_scm_info['rel_path'].replace(info['path'], '', 1)
            
        if os.path.isfile(log_xml_file):
            if stream_info["SCM_TYPE"] == "svn":
                tree = ET.ElementTree(file=log_xml_file)
                for elem in tree.iter():
                    if "url" == elem.tag:
                        file_scm_info['url']=elem.text.replace('\\','/')
                    elif "commit" == elem.tag:
                        file_scm_info['revision'] = elem.attrib['revision']
                if 'REPO_URL_MAP' in stream_info and json.loads(stream_info['REPO_URL_MAP']) != {}:
                    repo_url_map = json.loads(stream_info['REPO_URL_MAP'])
                    for key in repo_url_map.keys():
                        if repo_url_map[key] in file_scm_info['url']:
                            file_scm_info['repo_id'] = key
            elif stream_info["SCM_TYPE"] == "git":
                if 'GIT_REPO_ALL_MAP' in stream_info and stream_info['GIT_REPO_ALL_MAP'] != {}:
                    file_scm_info['revision'] = linecache.getline(log_xml_file,1).strip()
                    git_repo_all_map = stream_info['GIT_REPO_ALL_MAP']
                    for key in git_repo_all_map.keys():
                        local_url = git_repo_all_map[key]['GIT_LOCAL_URL']
                        local_branch = git_repo_all_map[key]['GIT_LOCAL_BRANCH']
                        local_path = ''.join('/'+git_repo_all_map[key]['GIT_LOCAL_RELPATH']).replace('//','/')
                        if local_path in file_path:
                            file_scm_info['url'] = file_path.replace(local_path, local_url+'/').replace('//','/').replace('\\','/')
                            file_scm_info['branch'] = local_branch
                            file_scm_info['repo_id'] = key
                            break
                else:
                    file_scm_info['revision'] = linecache.getline(log_xml_file,1).strip()
                    root_path = file_path.replace(file_scm_info['rel_path'], '')
                    file_scm_info['url'] = file_path.replace(root_path, stream_info['GIT_LOCAL_URL']+'/').replace('//','/').replace('\\','/')
                    file_scm_info['branch'] = stream_info['GIT_LOCAL_BRANCH']
            
            if 'REPO_SCM_RELPATH_MAP' in stream_info and json.loads(stream_info['REPO_SCM_RELPATH_MAP']) != {} and 'repo_id' in file_scm_info:
                repo_scm_relpath_map = json.loads(stream_info['REPO_SCM_RELPATH_MAP'])
                for key in repo_scm_relpath_map.keys():
                    if key == file_scm_info['repo_id']:
                        file_scm_info['rel_path'] = ''.join(repo_scm_relpath_map[key]+'/'+file_scm_info['rel_path']).replace('//','/')
                        break
    except Exception as e:
        #raise Exception(e)
        pass
        
    return file_scm_info

def get_local_git_url(stream_code_path):
    info = {}
    info['GIT_LOCAL_URL'] = ''
    info['GIT_LOCAL_BRANCH'] = 'master'
    try:
        stream_code_path = stream_code_path.replace('//', '/')
        git_config_file = stream_code_path+'/.git/config'
        if os.path.exists(git_config_file):
            with open(git_config_file, "r", encoding = 'utf-8') as git_config:
                for line in git_config.readlines():
                    if "url =" in line:
                        info['GIT_LOCAL_URL'] = line.strip().replace(' ', '').replace('url=', '')
                    if 'branch' in line:
                        branch = line.strip().replace('[branch', '').replace('\"', '').replace(']','')
                        info['GIT_LOCAL_BRANCH'] = branch
    except Exception as e:
        raise Exception(e)
        
    return info
