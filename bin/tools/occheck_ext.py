import sys
sys.path.append("./common/")
import codecs
import json
import multiprocessing
import os
import pid_config
import re
import result
import subprocess
import util

def check():
    project_file_list = ""
    stream_result_path = ""
    pool_processes = ""
    pid_file = ""
    config_path = ""
    if 'PROJECT_FILE_LIST' in stream_info:
        project_file_list = stream_info['PROJECT_FILE_LIST']
    if 'STREAM_RESULT_PATH' in stream_info:
        stream_result_path = stream_info['STREAM_RESULT_PATH']
    if 'POOL_PROCESSES' in stream_info:
        pool_processes = stream_info['POOL_PROCESSES']
    if 'PID_FILE' in stream_info:
        pid_file = stream_info['PID_FILE']
    if 'CONFIG_PATH' in stream_info:
        config_path = stream_info['CONFIG_PATH']
    if project_file_list == '' or stream_result_path == '' or \
        pool_processes == '' or pid_file == '':
        print('below option is empty!')
        print('project_file_list: ' + project_file_list)
        print('stream_result_path: ' + stream_result_path)
        print('pool_processes: ' + pool_processes)
        print('pid_file: ' + pid_file)
        exit(1)

    scan_occheck_count = 0
    if os.path.isfile(project_file_list):
        with codecs.open(project_file_list, "r", encoding='utf-8') as file:
            process_analyze = multiprocessing.Pool(processes=int(pool_processes))
            for filename in file.readlines():
                filename = filename.strip()
                try:
                    scan_occheck_count += 1
                    process_analyze.apply_async(scan_occheck, (filename, stream_result_path, pid_file, config_path, ))
                except Exception as e:
                    print(e)
            process_analyze.close()
            process_analyze.join()
    #print("scan occheck file count: " + str(scan_occheck_count))
    return 0

def scan_occheck(filename, stream_result_path, pid_file, config_path):
    filename_result = result.get_result_file_path(stream_result_path, filename)
    occheck_err_file = filename_result + ".error"
    occheck_json = filename_result + ".json"
    #print("occheck scan: " + filename)
    current_path = sys.path[0] + '/../'
    occheck_bin = os.path.join(current_path, 'tools_dep/occheck')
    command = "python " + occheck_bin + "/occheck.py "+ filename + " --config " + config_path + " -f json -o " + occheck_json
    occheck_p_2 = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, \
        shell=True, start_new_session=True)
    try:
        pid_config.add_pid(str(occheck_p_2.pid), pid_file)
        for line in occheck_p_2.stdout:
            continue
    finally:
        occheck_p_2.terminate()
        occheck_p_2.wait()

    if os.path.isfile(occheck_json):
        try:
            with open(occheck_json, 'r', encoding='utf-8') as occheckjsonfile:
                parsed_json = json.load(occheckjsonfile)
                with open(occheck_err_file, 'w', encoding='utf-8') as logfile:
                    for checker_json in parsed_json:
                        logfile.write(filename + '->' + str(checker_json['Line']) + '->' + \
                            checker_json['CheckName'] + '->' + checker_json['Message'] + '\n')
        except Exception as e:
            print('=>occheck_ext.py->scan_occheck->ERROR: ' + str(e) + "->" + occheck_json)

if __name__ == "__main__" :
    stream_info = json.loads(util.base64todecode(sys.argv[1]))
    check()
