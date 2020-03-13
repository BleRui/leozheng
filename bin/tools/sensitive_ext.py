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

def get_tool_path():
    current_path = sys.path[0] + '/../'
    tool_path = os.path.join(current_path, 'tools_dep/sensitive/sensitive_info_detect')
    return tool_path

def check():
    project_file_list = ""
    stream_result_path = ""
    pool_processes = ""
    pid_file = ""
    stream_name = ""
    proj_owner = ""
    if 'PROJECT_FILE_LIST' in stream_info:
        project_file_list = stream_info['PROJECT_FILE_LIST']
    if 'STREAM_RESULT_PATH' in stream_info:
        stream_result_path = stream_info['STREAM_RESULT_PATH']
    if 'POOL_PROCESSES' in stream_info:
        pool_processes = stream_info['POOL_PROCESSES']
    if 'PID_FILE' in stream_info:
        pid_file = stream_info['PID_FILE']
    if 'STREAM_NAME' in stream_info:
        stream_name = stream_info['STREAM_NAME']
    if 'PROJ_OWNER' in stream_info:
        proj_owner = stream_info['PROJ_OWNER']

    if project_file_list == '' or stream_result_path == '' or pool_processes == '' or \
        pid_file == '' or stream_name == '' or proj_owner == '':
        print('below option is empty!')
        print('project_file_list: ' + project_file_list)
        print('stream_result_path: ' + stream_result_path)
        print('pool_processes: ' + pool_processes)
        print('pid_file: ' + pid_file)
        print('stream_name: ' + stream_name)
        print('proj_owner: ' + proj_owner)
        exit(1)

    scan_sensitive_count = 0
    if os.path.isfile(project_file_list):
        with codecs.open(project_file_list, "r", encoding='utf-8') as file:
            process_analyze = multiprocessing.Pool(processes=int(pool_processes))
            tool_path = get_tool_path()
            os.chmod(tool_path, 0o755)
            for filename in file.readlines():
                filename = filename.strip()
                try:
                    scan_sensitive_count += 1
                    process_analyze.apply_async(scan_sensitive, (filename, stream_info))
                except Exception as e:
                    print(e)
            process_analyze.close()
            process_analyze.join()
    #print("scan sensitive file count: " + str(scan_sensitive_count))
    return 0

def scan_sensitive(filename, stream_info):
    stream_result_path = stream_info['STREAM_RESULT_PATH']
    pid_file = stream_info['PID_FILE']
    stream_name = stream_info['STREAM_NAME']
    proj_owner = stream_info['PROJ_OWNER']
    proj_owner = proj_owner.replace(';', ',')
    skip_checkers = []
    if 'SKIP_CHECKERS' in stream_info and stream_info['SKIP_CHECKERS'] != "":
        skip_checkers = stream_info['SKIP_CHECKERS'].split(";")
    filename_result = result.get_result_file_path(stream_result_path, filename)
    sensitive_err_file = filename_result + ".error"
    sensitive_json = filename_result + ".json"
    #print("sensitive scan: " + filename)
    tool_path = get_tool_path()
    command = tool_path + " " + stream_name + " " + \
        proj_owner + " " + filename + " -f " + sensitive_json
    sensitive_p_2 = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, \
        shell=True, start_new_session=True)
    try:
        pid_config.add_pid(str(sensitive_p_2.pid), pid_file)
        for line in sensitive_p_2.stdout:
            continue
            #line = str(line.decode('utf-8'))
            #print(line)
    finally:
        sensitive_p_2.terminate()
        sensitive_p_2.wait()

    if os.path.isfile(sensitive_json):
        with open(sensitive_json, 'r', encoding='utf-8') as sensitivejsonfile:
            try:
                reg = re.search("(?<=scan_result:).*", sensitivejsonfile.read())
                parsed_json = reg.group(0) if reg else "{ }"
                parsed_json = json.loads(parsed_json)
                with open(sensitive_err_file, 'w', encoding='utf-8') as logfile:
                    if "check_report" in parsed_json:
                        for file_json in parsed_json["check_report"]:
                            if not str(file_json['rule_name']) in skip_checkers:
                                logfile.write(filename + '->' + str(file_json['line_no']) + '->' + \
                                    str(file_json['rule_name']) + '->' + \
                                        str(file_json['explanation']) + '\n')
            except Exception as e:
                print('=>sensitive_ext.py->scan_sensitive->ERROR: ' + str(e) + "->" + \
                    sensitive_json + "->" + sensitive_json.read())

if __name__ == "__main__" :
    stream_info = json.loads(util.base64todecode(sys.argv[1]))
    check()
