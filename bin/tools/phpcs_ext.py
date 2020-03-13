import sys
sys.path.append("./common/")
import codecs
import json
import multiprocessing
import os
import pid_config
import result
import subprocess
import util
import xml.etree.ElementTree as ET

def check():
    project_file_list = ""
    stream_result_path = ""
    pool_processes = ""
    pid_file = ""
    phpcs_standard = ""
    if 'PROJECT_FILE_LIST' in stream_info:
        project_file_list = stream_info['PROJECT_FILE_LIST']
    if 'STREAM_RESULT_PATH' in stream_info:
        stream_result_path = stream_info['STREAM_RESULT_PATH']
    if 'POOL_PROCESSES' in stream_info:
        pool_processes = stream_info['POOL_PROCESSES']
    if 'PID_FILE' in stream_info:
        pid_file = stream_info['PID_FILE']
    if 'PHPCS_STANDARD' in stream_info:
        phpcs_standard = stream_info['PHPCS_STANDARD']
    if project_file_list == '' or stream_result_path == '' or \
        pool_processes == '' or pid_file == '' or phpcs_standard == '':
        print('below option is empty!')
        print('project_file_list: ' + project_file_list)
        print('stream_result_path: ' + stream_result_path)
        print('pool_processes: ' + pool_processes)
        print('pid_file: ' + pid_file)
        print('phpcs_standard: ' + phpcs_standard)
        exit(1)

    scan_phpcs_count = 0
    if os.path.isfile(project_file_list):
        with codecs.open(project_file_list, "r", encoding='utf-8') as file:
            process_analyze = multiprocessing.Pool(processes=int(pool_processes))
            for filename in file.readlines():
                filename = filename.strip()
                try:
                    scan_phpcs_count += 1
                    process_analyze.apply_async(scan_phpcs, (filename, stream_info))
                except Exception as e:
                    print(e)
            process_analyze.close()
            process_analyze.join()
    #print("scan phpcs file count: " + str(scan_phpcs_count))
    return 0

def scan_phpcs(filename, stream_info):
    stream_result_path = stream_info['STREAM_RESULT_PATH']
    pid_file = stream_info['PID_FILE']
    phpcs_standard = stream_info['PHPCS_STANDARD']
    skip_checkers = []
    if 'SKIP_CHECKERS' in stream_info and stream_info['SKIP_CHECKERS'] != "":
        skip_checkers = stream_info['SKIP_CHECKERS'].split(";")
    filename_result = result.get_result_file_path(stream_result_path, filename)
    phpcs_err_file = filename_result + ".error"
    phpcs_xml = filename_result + ".xml"
    #print("phpcs scan: " + filename)
    current_path = sys.path[0] + '/../'
    phpcs_bin = os.path.join(current_path, 'tools_dep/phpcs')
    command = "php " + phpcs_bin + "/phpcs.phar " + "--standard=" + phpcs_standard + " " + \
        filename + " --report=xml > " + phpcs_xml
    phpcs_p_2 = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, \
        shell=True, start_new_session=True)
    try:
        pid_config.add_pid(str(phpcs_p_2.pid), pid_file)
        for line in phpcs_p_2.stdout:
            line = str(line.decode('utf-8'))
            print(line)
    finally:
        phpcs_p_2.terminate()
        phpcs_p_2.wait()

    if os.path.isfile(phpcs_xml):
        try:
            with open(phpcs_err_file, 'w', encoding='utf-8') as logfile:
                tree = ET.ElementTree(file=phpcs_xml)
                for elem in tree.iter():
                    if (elem.tag == "error" or elem.tag == "warning") and \
                        not elem.attrib['source'] in skip_checkers:
                        logfile.write(filename + '->' + elem.attrib['line'] + '->' + \
                            elem.attrib['source'] + '->' + elem.text + '\n')
        except Exception as e:
            print('=>phpcs_ext.py->scan_phpcs->ERROR: ' + str(e) + "->" + phpcs_xml)

if __name__ == "__main__" :
    stream_info = json.loads(util.base64todecode(sys.argv[1]))
    check()
