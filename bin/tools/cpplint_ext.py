#check all files cpplint issues in folder and output a xml report
import sys
sys.path.append("../common/")
sys.path.append("../tools_dep/cpplint")
import xml
from xml.dom import minidom
import codecs
import os
import stat
import platform
import datetime
import subprocess
import multiprocessing
import result
import json
import util

reload(sys)
os_type = platform.system()
if os_type == "Windows":
    sys.setdefaultencoding('gbk')
else:
    sys.setdefaultencoding('utf-8')

_proj_code_root = 'src'

stream_info = {}

def check():
    project_file_list = ""
    stream_result_path = ""
    pool_processes = ""
    skip_filters = ""
    cpplint_file="cpplint"
    current_path=sys.path[0]
    open_checkers=''
    checkers_options = ''
    if 'SPECIFIED_FOR_PROJECT' in stream_info and stream_info['SPECIFIED_FOR_PROJECT'] != "":
        project_list = stream_info['SPECIFIED_FOR_PROJECT'].split(";")
        stream_name = stream_info['STREAM_NAME']
        for project in project_list:
            if stream_name == project:
                cpplint_file = "cpplint"+"_"+stream_name
                if not os.path.exists(current_path+'/../tools_dep/cpplint/'+cpplint_file+".py"):
                    print("can not found the "+current_path+'/../tools_dep/cpplint/'+cpplint_file+".py")
                    exit(1)
                break
    if 'PROJECT_FILE_LIST' in stream_info:
        project_file_list = stream_info['PROJECT_FILE_LIST']
    if 'STREAM_RESULT_PATH' in stream_info:
        stream_result_path = stream_info['STREAM_RESULT_PATH']
    if 'POOL_PROCESSES' in stream_info:
        pool_processes = stream_info['POOL_PROCESSES']
    if 'SKIP_CHECKERS' in stream_info and stream_info['SKIP_CHECKERS'].replace(" ", "") != '':
        if stream_info['SKIP_CHECKERS'].endswith(';'):
            stream_info['SKIP_CHECKERS'] = stream_info['SKIP_CHECKERS'][:-1]
        skip_filters = '-'+stream_info['SKIP_CHECKERS'].replace(" ", "").replace(";", ",-")
    if 'OPEN_CHECKERS' in stream_info and stream_info['OPEN_CHECKERS'].replace(" ", "") != '':
        if stream_info['OPEN_CHECKERS'].endswith(';'):
            stream_info['OPEN_CHECKERS'] = stream_info['OPEN_CHECKERS'][:-1]
        open_checkers = '+'+stream_info['OPEN_CHECKERS'].replace(" ", "").replace(";", ",+")

    if 'CHECKER_OPTIONS' in stream_info and stream_info['CHECKER_OPTIONS'] != '' and cpplint_file == 'cpplint':
        checker_options = json.loads(stream_info['CHECKER_OPTIONS'])
        for checker_option in checker_options.values():
            checker_option = json.loads(checker_option)
            keys = checker_option.keys()
            for key in keys:
                checkers_options += ' --'+key+'='+checker_option[key]
                
    if project_file_list == '' or stream_result_path == '' or pool_processes == '':
        print('below option is empty!')
        print('project_file_list: '+project_file_list)
        print('stream_result_path: '+stream_result_path)
        print('pool_processes: '+pool_processes)
        exit(1)
    
    scan_cpplint_count =0
    if os.path.isfile(project_file_list):
        with codecs.open(project_file_list, "r", encoding = 'utf-8') as file:
            process_analyze = multiprocessing.Pool(processes = int(pool_processes))
            for filename in file.readlines():
                filename = filename.strip()
                try:
                    scan_cpplint_count +=1
                    #print('begin analyze file :%s' %(filename.strip()))
                    process_analyze.apply_async(scan_cpplint, (cpplint_file, filename, stream_result_path, skip_filters,open_checkers,checkers_options, ))
                except Exception as e:
                        print(e)
            process_analyze.close()
            process_analyze.join()  
    #print("scan cpplint file count: "+str(scan_cpplint_count))
    return 0

def scan_cpplint(cpplint_file, filename, stream_result_path,skip_filters,open_checkers,checkers_options):
    filename_result = result.get_result_file_path(stream_result_path,filename)
    cpplint_error_file = filename_result+".error"
    filters = '--filter='+skip_filters+','+open_checkers
    cpplint_path=sys.path[0]+'/../tools_dep/cpplint/'+cpplint_file+".py"
    command = "python "+cpplint_path+" --output=codecc "+checkers_options+"  "+filters+" "+filename+" >"+cpplint_error_file+' 2>&1'
    os.system(command)

if __name__ == "__main__" :
    stream_info = json.loads(util.base64todecode(sys.argv[1]))
    check()