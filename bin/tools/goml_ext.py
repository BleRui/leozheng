import sys,platform
sys.path.append("./common/")
import os
import json
import pid_config
import subprocess
import codecs
import result
import util
import re
import file
#import codecc_web

bug_arrary = set([])
go_build_faild_skip_error=['cannot find package', 'invalid operation:', 'cannot range over']
default_skip_linter = ['lll', 'gocyclo', 'testify', 'test', 'dupl', 'gotypex', 'megacheck', 'goimports']
go_build_faild_skip_linter=['maligned','varcheck','structcheck','unparam','errcheck','gotype','interfacer','unconvert'] 
go_build_status = 'true'

def check():
    global go_build_status
    stream_code_path = ""
    project_goml_json = ""
    skip_paths = "" #添加过滤路径
    default_disable_linter = "" #获取默认屏蔽linter列表
    build_failed_disable_linter = "" #获取编译失败屏蔽linter列表  
    stream_result_path = ""
    current_path=sys.path[0]
    scan_path= ""
    go_path = ""
    bug_data_list = []
    go_build_message = ""
    checkers_options = ''
    scan_finish_message = ''
    
    if 'STREAM_CODE_PATH' in stream_info:
        stream_code_path = stream_info['STREAM_CODE_PATH']  
    if 'PROJECT_GOML_JSON' in stream_info:
        project_goml_json = stream_info['PROJECT_GOML_JSON']
    for linter in default_skip_linter:
        default_disable_linter += " --disable="+linter+" "
    if 'STREAM_RESULT_PATH' in stream_info:
        stream_result_path = stream_info['STREAM_RESULT_PATH']
    if "GOROOT" in stream_info:
        os.environ["GOROOT"]= stream_info['GOROOT']
    if "GO15VENDOREXPERIMENT" in stream_info:
        os.environ["GO15VENDOREXPERIMENT"]= stream_info['GO15VENDOREXPERIMENT']

    if 'SUB_CODE_PATH_LIST' in stream_info and stream_info['SUB_CODE_PATH_LIST'] != '':
        sub_code_path_list = stream_info['SUB_CODE_PATH_LIST'].split(',')
        sub_path_list = [''.join(stream_code_path+'/'+path).replace('//','/') for path in sub_code_path_list]
        find_path = stream_code_path
        stream_info['SKIP_PATHS'] += util.add_skip_path('', stream_code_path, find_path, sub_path_list)

    if "SKIP_PATHS" in stream_info:
        skip_path_list = stream_info['SKIP_PATHS'].split(';')
        for skip_path in skip_path_list:
            skip_path = skip_path.replace(".*/",'').replace("/.*",'').replace(".*",'').replace("*",'')
            if  skip_path.replace(' ', '') == "":
                continue
            if re.search("^src/", skip_path):
                skip_path = skip_path[4:]
            skip_paths += " --skip=\""+skip_path+"\" "
    
    if 'CHECKER_OPTIONS' in stream_info and stream_info['CHECKER_OPTIONS'] != '':
        checker_options = json.loads(stream_info['CHECKER_OPTIONS'])
        for checker_option in checker_options.values():
            checker_option = json.loads(checker_option)
            keys = checker_option.keys()
            for key in keys:
                checkers_options += ' --'+key+'='+checker_option[key]
    
    if stream_code_path == '' or project_goml_json == '' or stream_result_path == '':
        print('below option is empty!')
        print('stream_code_path: '+stream_code_path)
        print('project_goml_json: '+project_goml_json)
        print('stream_result_path: '+stream_result_path)
        exit(1)
    
    go_path=stream_code_path
    workspace=stream_code_path
    if "REL_PATH" in stream_info and stream_info['REL_PATH'] != '':
        go_path = ''.join(go_path.replace(stream_info['REL_PATH'], ''))
        workspace = go_path
    if "GO_PATH" in stream_info and stream_info['GO_PATH'] != '':
        rel_go_path_list = stream_info['GO_PATH'].split(';')
        for rel_go_path in rel_go_path_list:
            if os.path.exists(workspace +'/'+rel_go_path):
                go_path += os.pathsep+workspace +'/'+rel_go_path
    os.environ["GOPATH"] = go_path

    os.chdir(stream_code_path)
    print('GOPATH: '+go_path)

    command = "go build ./..."
    go_build_p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,shell=True,start_new_session=True,env=dict(os.environ, LANG="C", LC_ALL="C"))
    try:
        pid_config.add_pid(str(go_build_p.pid), stream_info["PID_FILE"])
        for line in go_build_p.stdout:
            line = str(line.decode('utf-8'))
            if "" != line and 'GOPATH' in line:
                go_build_message += line.replace(workspace, '$WORKSPACE').replace('(from $GOPATH)', '')
    finally:
        go_build_p.terminate()
        go_build_p.wait()
    
    if "WORKSPACE" in go_build_message:
        scan_finish_message += "Please check your GOPATH para in CodeCC. If you don't upload all golang dependent libraries to svn/git, please ignore this warning. \nCannot find below package: \n"+go_build_message
        print(scan_finish_message)
        if 'STREAM_DATA_PATH' in stream_info and os.path.exists(stream_info['STREAM_DATA_PATH']):
            with open(stream_info['STREAM_DATA_PATH']+'/go_build.log', "w", encoding = 'utf-8') as go_build_file:
                go_build_file.write(scan_finish_message)
        go_build_status = 'false'
        
    if 'false' == go_build_status:
        for linter in go_build_faild_skip_linter:
            build_failed_disable_linter += " --disable="+linter+" " 


    #codecc_web.upload_goml_project_dir_struct_checker(stream_info['TOOL_TYPE'].upper(), 'true', 'true')

    print("go gometalinter ./...")  
    command="gometalinter ./... --sort=path --deadline=60m --json --enable-all "+checkers_options+default_disable_linter+" "+build_failed_disable_linter+" "+skip_paths+" --exclude=vendor -j 2"
    goml_p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,shell=True,start_new_session=True)
    try:
        pid_config.add_pid(str(goml_p.pid), stream_info["PID_FILE"])
        for line in goml_p.stdout:
            line = str(line.decode('utf-8'))

            #过滤不是告警行
            if not 'severity' in line:
                continue
            
            result = json.loads(line.replace('},','}')) 
            
            if 'vet' == result['linter']:
                result['message'] = 'vet/vet->'+result['message']
            
            if 'gas' == result['linter']:
                result['message'] = result['message'].replace(',xxx', '')
            
            if build_error_check(result, stream_info):
                continue

            #print(util.get_datetime()+" "+line)
            bug_data_list.append(result)
                
        with open(project_goml_json, "a+", encoding = 'utf-8') as file:
            if len(bug_data_list) > 0:
                file.write(json.dumps(bug_data_list))
    finally:
        goml_p.terminate()
        goml_p.wait()
        os.chdir(current_path)
        
    parse_project_goml_json_file_list(stream_info)
    
    parse_project_goml_json_file_error(stream_info)
    
def build_error_check(result, stream_info):
    
    global go_build_status
    if 'gotype' == result['linter'] and "could not import" in result['message']:
        return True
    
    if "error:" in result['message'] and "No such file or directory" in result['message']:
        return True
        
    if "unknown field" in result['message'] and "struct literal" in result['message']:
        return True
        
    if "not declared by package" in result['message']:
        return True 
        
    if not '->' in result['message']:
        return True
        
    #对内容重复的告警进行去重
    if result['path']+'->'+str(result['line'])+'->'+result['message'] in bug_arrary:
        return True
    else:
        bug_arrary.add(result['path']+'->'+str(result['line'])+'->'+result['message'])

    #过滤编译失败出现的无效告警
    for go_build_failed_error in go_build_faild_skip_error:
        if go_build_failed_error in result['message']:
            return True
    
    #去除默认屏蔽linter告警：
    for skip_check in default_skip_linter:
        if skip_check in result['linter']:
            return True         
    
    #去除编译失败屏蔽linter告警：
    if 'false' == go_build_status:
        for skip_check in go_build_faild_skip_linter:
            if skip_check in result['linter']:
                return True
    
    #实现自定义过滤规则
    if 'SKIP_CHECKERS' in stream_info and "" != stream_info['SKIP_CHECKERS']:
        for skip_check in stream_info['SKIP_CHECKERS'].split(';'):
            if skip_check != '' and  skip_check+'->' in result['message']:
                return True
    
    return False
    
def get_go_path(stream_code_path):
    go_path = stream_code_path
    src_paths = file.find_path_return_array(stream_code_path, 'src', set([]))
    for path in src_paths:
        if not path in go_path.split(':'):
            go_path +=':'+path
    return go_path

def parse_project_goml_json_file_list(stream_info):
    scan_path=stream_info['STREAM_CODE_PATH']
    project_goml_json = stream_info['PROJECT_GOML_JSON']
    skip_path_list = stream_info['SKIP_PATHS'].split(';')
    subfix_list = stream_info['TARGET_SUBFIXS'].split(';')
    skip_paths = []
    for skip_path in skip_path_list:
        skip_path = skip_path.replace(".*",'')
        if  skip_path.replace(' ', '') == "":
            continue
        for subfix in subfix_list: 
            if re.search("."+subfix.strip()+"$", skip_path):
                skip_paths.append(skip_path)

    sort_file_paths=set([])
    if os.path.isfile(project_goml_json) and os.path.getsize(project_goml_json):
        with open(project_goml_json, "r", encoding = 'utf-8') as jsonfile:
            all_result_json = json.load(jsonfile)
            for line in all_result_json:
                for skp in skip_paths:
                    if re.search(skp+"$", scan_path+'/'+line["path"]):
                        break
                else:
                    sort_file_paths.add(scan_path+'/'+line["path"])
    with open(stream_info['PROJECT_FILE_LIST'], "a+", encoding = 'utf-8') as file_list:
        for sourcefile in sort_file_paths:
            file_list.write(sourcefile+"\n")
            
def parse_project_goml_json_file_error(stream_info):
    scan_path=stream_info['STREAM_CODE_PATH']
    project_goml_json = stream_info['PROJECT_GOML_JSON']
    if os.path.isfile(project_goml_json) and os.path.getsize(project_goml_json):
        with open(project_goml_json, "r", encoding = 'utf-8') as jsonfile:
            all_result_json = json.load(jsonfile)
            for line in all_result_json:
                file_path = scan_path+'/'+line["path"]
                filename_result = result.get_result_file_path(stream_info['STREAM_RESULT_PATH'], file_path)
                file_error_path = filename_result+'.error'
                error_line = str(file_path)+'->'+str(line["line"])+'->'+str(line["linter"])+'->'+str(line["message"])+''
                try:
                    with open(file_error_path, "a+", encoding = 'utf-8') as file_list:
                        file_list.write(error_line+"\n")
                except Exception as e:
                    print("=>main.py->parse_project_goml_json_file_error->ERROR:"+str(e)+file_error_path)
                    
if __name__ == "__main__" :
    stream_info = json.loads(util.base64todecode(sys.argv[1]))
    check()
