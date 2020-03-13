import sys,platform
sys.path.append("./common/")
import pid_config
import os
import json
import subprocess
import multiprocessing
import codecs
import result
import util
import platform
import xml.etree.ElementTree as ET
import re
import file
os_type = platform.system()

def check():
    current_path=sys.path[0]
    project_file_list = ""
    stream_result_path = ""
    pool_processes = ""
    skip_filters = ""
    pid_file = ""
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
    if 'CONFIG_PATH' in stream_info:
        config_path = stream_info['CONFIG_PATH']
    if 'STREAM_CODE_PATH' in stream_info:
        stream_code_path = stream_info['STREAM_CODE_PATH']
    if project_file_list == '' or stream_result_path == '' or pool_processes == '' or pid_file == '':
        print('below option is empty!')
        print('project_file_list: '+project_file_list)
        print('stream_result_path: '+stream_result_path)
        print('pool_processes: '+pool_processes)
        print('pid_file: '+pid_file)
        exit(1)

    os.chdir(stream_code_path)
    #运行编译命令
    if 'PROJECT_BUILD_COMMAND' in stream_info:
        os.system(stream_info['PROJECT_BUILD_COMMAND'])
    
    #配置project_class_file_list
    stream_info['PROJECT_CLASS_FILE_LIST'] = os.path.join(stream_info["STREAM_DATA_PATH"], 'project_class_file_list.txt')
    
    #生成class文件列表
    file.general_class_list_file(stream_info)
    
    #如果无project_class_file_list返回
    if not os.path.isfile(stream_info['PROJECT_CLASS_FILE_LIST']):
        return 
        
    current_path = sys.path[0] + '/../'
    spotbugs_lib = os.path.join(current_path, 'tools_dep/spotbugs/lib')
    spotbugs_ouput_xml = os.path.join(stream_info["STREAM_DATA_PATH"], 'spotbugs_ouput.xml')
    
    command = 'java -jar '+spotbugs_lib+'/spotbugs.jar -textui  -include '+config_path+' -xdocs  -output '+spotbugs_ouput_xml+' -analyzeFromFile '+stream_info['PROJECT_CLASS_FILE_LIST']
    
    spotbugs_p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, \
        shell=True, start_new_session=True)
    try:
        pid_config.add_pid(str(spotbugs_p.pid), pid_file)
        for line in spotbugs_p.stdout:
            pass
    finally:
        spotbugs_p.terminate()
        spotbugs_p.wait()
        os.chdir(current_path)
        
    if os.path.isfile(spotbugs_ouput_xml):
        try:
            sub_root = ET.ElementTree(file=spotbugs_ouput_xml).getroot()
            for elem in sub_root.findall("file"):
                try:
                    reg_path = elem.attrib['classname'].replace('.','/')+'.java'
                    file_path = file.find_project_file_list_path(reg_path, project_file_list)
                    if '' == file_path:
                        continue
                    filename_result = result.get_result_file_path(stream_result_path,file_path)
                    spotbugs_err_file = filename_result+".error"
                    with open(spotbugs_err_file, 'w', encoding='utf-8') as logfile:
                        for sub_elem in elem.iter(): 
                            try:
                                logfile.write(file_path + '->' + sub_elem.attrib['line'] + '->' + sub_elem.attrib['type'] + '->' + sub_elem.attrib['message'] + '\n')
                            except:
                                pass
                except:
                    pass
        except Exception as e:
            print('=>spotbugs_ext.py->check->ERROR: ' + str(e) + "->" + spotbugs_ouput_xml)

if __name__ == "__main__" :
    stream_info = json.loads(util.base64todecode(sys.argv[1]))
    check()
