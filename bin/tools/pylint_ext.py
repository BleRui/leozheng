import sys,platform
sys.path.append("./common/")
import os
import json
import pid_config
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
    disable_option = ""
    pylint_path = ""
    py_path = ""
    pid_file = ""
    config_path = ""
    if 'PROJECT_FILE_LIST' in stream_info:
        project_file_list = stream_info['PROJECT_FILE_LIST']
    if 'STREAM_RESULT_PATH' in stream_info:
        stream_result_path = stream_info['STREAM_RESULT_PATH']
    if 'POOL_PROCESSES' in stream_info:
        pool_processes = stream_info['POOL_PROCESSES']
    if 'SKIP_CHECKERS' in stream_info:
        skip_filters = stream_info['SKIP_CHECKERS'].replace(";", ",")
    if skip_filters != "":
        disable_option = "--disable="+skip_filters
    if 'PID_FILE' in stream_info:
        pid_file = stream_info['PID_FILE']
    if 'CONFIG_PATH' in stream_info:
        config_path = stream_info['CONFIG_PATH']
    if "PY_VERSION" in stream_info and stream_info["PY_VERSION"] == 'py2':
        pylint_path = stream_info["PY27_PYLINT_PATH"]
        py_path = stream_info["PY27_PATH"]
    else:
        pylint_path = stream_info["PY35_PYLINT_PATH"]
        py_path = stream_info["PY35_PATH"]
        
    if project_file_list == '' or stream_result_path == '' or pool_processes == '' or pylint_path == '' or py_path == '' or pid_file == '':
        print('below option is empty!')
        print('project_file_list: '+project_file_list)
        print('stream_result_path: '+stream_result_path)
        print('pool_processes: '+pool_processes)
        print('pylint_path: '+pylint_path)
        print('py_path: '+py_path)
        print('pid_file: '+pid_file)
        exit(1)

    os.environ["PATH"] = py_path + os.pathsep + os.environ["PATH"]
    
    scan_pylint_count=0
    if os.path.isfile(project_file_list):
        with codecs.open(project_file_list, "r", encoding = 'utf-8') as file:
            process_analyze = multiprocessing.Pool(processes = int(pool_processes))
            for filename in file.readlines():
                filename = filename.strip()
                try:
                    scan_pylint_count+=1
                    process_analyze.apply_async(scan_pylint, (filename, pylint_path, stream_result_path, disable_option, py_path, pid_file,config_path,))
                except Exception as e:
                        print(e)
            process_analyze.close()
            process_analyze.join() 
    #print("scan pylint file count: "+str(scan_pylint_count))
    return 0

def scan_pylint(filename, pylint_path, stream_result_path, disable_option, py_path,pid_file,config_path):
    filename_result = result.get_result_file_path(stream_result_path,filename)
    pylint_err_file = filename_result+".error"
    pylint_json = filename_result+".json"
    
    command = "python lint.py --output-format=json --reports=n --rcfile "+config_path+" "+filename+" >"+pylint_json
    try:
        os.chdir(pylint_path)
        #print("pylint scan: "+filename)
        pylint_p_2 = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,shell=True,start_new_session=True)
        pid_config.add_pid(str(pylint_p_2.pid), pid_file)
        for line in pylint_p_2.stdout:
            print(line)
    finally:
        pylint_p_2.terminate()
        pylint_p_2.wait()
    
    #print("parse json: "+pylint_json)
    if os.path.isfile(pylint_json):
        with open(pylint_json, 'r', encoding = 'utf-8') as pylintjsonfile:
            try:
                parsed_json = json.load(pylintjsonfile) 
                with open(pylint_err_file, 'w', encoding = 'utf-8') as logfile:
                    for line_json in parsed_json:
                        logfile.write(str(line_json["path"])+"->"+str(line_json["line"])+"->"+str(line_json["symbol"])+"->"+str(line_json["message"]).replace("\n", "\\n")+"\n")
            except ValueError:
                #print("parse json error, maybe empty :"+pylint_json)
                pass

if __name__ == "__main__" :
    stream_info = json.loads(util.base64todecode(sys.argv[1]))
    check()
