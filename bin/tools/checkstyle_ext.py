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
import platform
import xml.etree.ElementTree as ET
import re
os_type = platform.system()

def check():
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
    if project_file_list == '' or stream_result_path == '' or pool_processes == '' or pid_file == '':
        print('below option is empty!')
        print('project_file_list: '+project_file_list)
        print('stream_result_path: '+stream_result_path)
        print('pool_processes: '+pool_processes)
        print('pid_file: '+pid_file)
        exit(1)
        
    scan_checkstyle_count=0
    if os.path.isfile(project_file_list):
        with codecs.open(project_file_list, "r", encoding = 'utf-8') as file:
            process_analyze = multiprocessing.Pool(processes = int(pool_processes))
            for filename in file.readlines():
                filename = filename.strip()
                try:
                    scan_checkstyle_count+=1
                    process_analyze.apply_async(scan_checkstyle, (filename, stream_result_path, skip_filters, pid_file, config_path, ))
                except Exception as e:
                        print(e)
            process_analyze.close()
            process_analyze.join()  
    #print("scan checkstyle file count: "+str(scan_checkstyle_count))
    return 0


def scan_checkstyle(filename, stream_result_path, skip_filters, pid_file, config_path):
    filename_result = result.get_result_file_path(stream_result_path,filename)
    checkstyle_err_file = filename_result+".error"
    checkstyle_xml = filename_result+".xml"
    #print("checkstyle scan: "+filename)
    current_path=sys.path[0]+'/../'
    checkstyle_bin = os.path.join(current_path, 'tools_dep/checkstyle')
    classpath = ''
    if os_type == "Windows":
        classpath = checkstyle_bin+'/checkstyle-8.11-all.jar'
    else:
        classpath = checkstyle_bin+'/checkstyle-8.11-all.jar'
    command = "java  -classpath  "+classpath+" com.puppycrawl.tools.checkstyle.Main -c "+config_path+" -f xml "+filename+" >"+checkstyle_xml
    checkstyle_p_2 = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,shell=True,start_new_session=True)
    try:
        pid_config.add_pid(str(checkstyle_p_2.pid), pid_file)
        for line in checkstyle_p_2.stdout:
            print(line)
    finally:
        checkstyle_p_2.terminate()
        checkstyle_p_2.wait()

    
    with open(checkstyle_xml, "rU+",encoding= 'utf-8') as file:
        lines = file.readlines()
        for line in lines:
            if not re.search('^<', line):
                lines.remove(line)
        lines_str = ''.join(lines).strip()
        file.seek(0)
        file.truncate()
        file.write(lines_str)
        
    #print("parse xml: "+checkstyle_xml)
    disable_option_array = skip_filters.split(";")
    if os.path.isfile(checkstyle_xml):
        try:
            with open(checkstyle_err_file, 'w', encoding='utf-8') as logfile:
                tree = ET.ElementTree(file=checkstyle_xml)
                for elem in tree.iter():
                    if "error" == elem.tag:
                        #if elem.attrib['source'] in disable_option_array:
                        #   continue
                        logfile.write(filename+'->'+elem.attrib['line']+'->'+elem.attrib['source']+'->'+elem.attrib['message']+'\n')
        except Exception as e:
            print('=>checkstyle_ext.py->scan_checkstyle->ERROR:'+str(e)+checkstyle_xml)


if __name__ == "__main__" :
    stream_info = json.loads(util.base64todecode(sys.argv[1]))
    check()
