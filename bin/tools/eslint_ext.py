import sys,platform
sys.path.append("../common/")
import pid_config
import os
import json
import subprocess
import multiprocessing
import codecs
import result
import util

def check():
    project_file_list = ""
    stream_result_path = ""
    pool_processes = ""
    skip_filters = ""
    pid_file = ""
    eslintrc = ""
    config_path = ""
    if 'PROJECT_FILE_LIST' in stream_info:
        project_file_list = stream_info['PROJECT_FILE_LIST']
    if 'STREAM_RESULT_PATH' in stream_info:
        stream_result_path = stream_info['STREAM_RESULT_PATH']
    if 'POOL_PROCESSES' in stream_info:
        pool_processes = stream_info['POOL_PROCESSES']
    if 'SKIP_CHECKERS' in stream_info:
        skip_filters = stream_info['SKIP_CHECKERS']
    if 'PID_FILE' in stream_info:
        pid_file = stream_info['PID_FILE']
    if 'ESLINT_RC' in stream_info:
        eslintrc = stream_info['ESLINT_RC']
    if 'CONFIG_PATH' in stream_info:
        config_path = stream_info['CONFIG_PATH']
    if project_file_list == '' or stream_result_path == '' or pool_processes == '' or pid_file == '' or eslintrc == '':
        print('below option is empty!')
        print('project_file_list: '+project_file_list)
        print('stream_result_path: '+stream_result_path)
        print('pool_processes: '+pool_processes)
        print('pid_file: '+pid_file)
        print('eslintrc: '+eslintrc)
        exit(1)
        
    scan_eslint_count=0
    if os.path.isfile(project_file_list):
        with codecs.open(project_file_list, "r", encoding = 'utf-8') as file:
            process_analyze = multiprocessing.Pool(processes = int(pool_processes))
            for filename in file.readlines():
                filename = filename.strip()
                try:
                    scan_eslint_count+=1
                    process_analyze.apply_async(scan_eslint, (filename, eslintrc, stream_result_path, skip_filters, pid_file,config_path, ))
                except Exception as e:
                        print(e)
            process_analyze.close()
            process_analyze.join()  
    #print("scan eslint file count: "+str(scan_eslint_count))
    return 0


def scan_eslint(filename, eslintrc, stream_result_path, skip_filters, pid_file, config_path):
    filename_result = result.get_result_file_path(stream_result_path,filename)
    eslint_err_file = filename_result+".error"
    eslint_json = filename_result+".json"
    #print("eslint scan: "+filename)
    current_path=sys.path[0]+'/../'
    eslint_bin = os.path.join(current_path, 'tools_dep/eslintrc')
    command = "eslint --no-eslintrc -f json -c "+config_path+" "+filename+" >"+eslint_json
    #print(command)
    eslint_p_2 = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,shell=True,start_new_session=True)
    try:
        pid_config.add_pid(str(eslint_p_2.pid), pid_file)
        for line in eslint_p_2.stdout:
            if 'RangeError' in line:
                return
            print(line)
    finally:
        eslint_p_2.terminate()
        eslint_p_2.wait()
    
    #print("parse json: "+eslint_json)
    disable_option_array = skip_filters.split(";")
    if os.path.isfile(eslint_json):
        with open(eslint_json, 'r', encoding='utf-8') as eslintjsonfile:
            try:
                parsed_json = json.load(eslintjsonfile) 
                with open(eslint_err_file, 'w', encoding='utf-8') as logfile:
                    for file_json in parsed_json:
                        path = file_json["filePath"]
                        error_list = file_json["messages"]
                        for line_json in error_list:
                            #if not line_json["ruleId"] in disable_option_array:
                            logfile.write(str(path)+"->"+str(line_json["line"])+"->"+str(line_json["ruleId"])+"->"+str(line_json["message"])+"->"+str(line_json["nodeType"])+"->"+str(line_json["column"]).replace("\n", "\\n")+"\n")
            except ValueError:
                print("parse json error, maybe empty :"+eslint_json)

if __name__ == "__main__" :
    stream_info = json.loads(util.base64todecode(sys.argv[1]))
    check()
