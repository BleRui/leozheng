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
import xml.etree.ElementTree as ET

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

    scan_detekt_count = 0
    if os.path.isfile(project_file_list):
        with codecs.open(project_file_list, "r", encoding='utf-8') as file:
            process_analyze = multiprocessing.Pool(processes=int(pool_processes))
            for filename in file.readlines():
                filename = filename.strip()
                try:
                    scan_detekt_count += 1
                    process_analyze.apply_async(scan_detekt, (filename, stream_result_path, pid_file, config_path, ))
                except Exception as e:
                    print(e)
            process_analyze.close()
            process_analyze.join()
    #print("scan detekt file count: " + str(scan_detekt_count))
    return 0

def scan_detekt(filename, stream_result_path, pid_file, config_path):
    filename_result = result.get_result_file_path(stream_result_path, filename)
    detekt_err_file = filename_result + ".error"
    detekt_xml = filename_result + ".xml"
    #print("detekt scan: " + filename)
    current_path = sys.path[0] + '/../'
    detekt_bin = os.path.join(current_path, 'tools_dep/detekt')
    command = "java -jar " + detekt_bin + "/detekt-cli-1.0.0-RC14-all.jar " + "-i " + \
        filename + " -c " + config_path + " -r xml:" + detekt_xml
    detekt_p_2 = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, \
        shell=True, start_new_session=True)
    try:
        pid_config.add_pid(str(detekt_p_2.pid), pid_file)
        for line in detekt_p_2.stdout:
            pass
    finally:
        detekt_p_2.terminate()
        detekt_p_2.wait()

    if os.path.isfile(detekt_xml):
        try:
            with open(detekt_err_file, 'w', encoding='utf-8') as logfile:
                tree = ET.ElementTree(file=detekt_xml)
                for elem in tree.iter():
                    if elem.tag == "error":
                        checker = elem.attrib['source'].replace("detekt.", "")
                        logfile.write(filename + '->' + elem.attrib['line'] + '->' + \
                            checker + '->' + elem.attrib['message'] + '\n')
        except Exception as e:
            print('=>detekt_ext.py->scan_detekt->ERROR: ' + str(e) + "->" + detekt_xml)

if __name__ == "__main__" :
    stream_info = json.loads(util.base64todecode(sys.argv[1]))
    check()
