import sys
sys.path.append("../common/")
import pid_config
import os
import subprocess
import multiprocessing
import codecs
import result
import util
import json

def check():
    project_file_list = ""
    stream_result_path = ""
    pool_processes = ""
    pid_file = ""
    ccn_number = ""
    
    if 'PROJECT_FILE_LIST' in stream_info:
        project_file_list = stream_info['PROJECT_FILE_LIST']
    if 'STREAM_RESULT_PATH' in stream_info:
        stream_result_path = stream_info['STREAM_RESULT_PATH']
    if 'POOL_PROCESSES' in stream_info:
        pool_processes = stream_info['POOL_PROCESSES']
    if 'PID_FILE' in stream_info:
        pid_file = stream_info['PID_FILE']
    if 'CCN_NUMBER' in stream_info:
        ccn_number = stream_info['CCN_NUMBER']
        
    if project_file_list == '' or stream_result_path == '' or pool_processes == '' or pid_file == '' or ccn_number == '':
        print('below option is empty!')
        print('project_file_list: '+project_file_list)
        print('stream_result_path: '+stream_result_path)
        print('pool_processes: '+pool_processes)
        print('pid_file: '+pid_file)
        print('ccn_number: '+ccn_number)
        exit(1)
    
    scan_ccn_count=0
    if os.path.isfile(project_file_list):
        with codecs.open(project_file_list, "r", encoding = 'utf-8') as file:
            process_analyze = multiprocessing.Pool(processes = int(pool_processes))
            for filename in file.readlines():
                filename = filename.strip()
                try:
                    scan_ccn_count+=1
                    #print("ccn scan: "+filename.strip())
                    process_analyze.apply_async(scan_ccn, (filename, stream_result_path, pid_file, ccn_number, ))
                except Exception as e:
                        print(e)
            process_analyze.close()
            process_analyze.join()  
    #print("scan ccn file count: "+str(scan_ccn_count))
    return 0    

def scan_ccn(filename, stream_result_path, pid_file, ccn_number):
    filename_result = result.get_result_file_path(stream_result_path,filename)
    ccn_err_file = filename_result+".error"
    if os.path.isfile(filename):
        current_path=sys.path[0]+'/../'
        ccn_bin = os.path.join(current_path, 'tools_dep/lizard')
        command = "python "+ccn_bin+"/lizard.py "+filename+" -w -C "+ccn_number+" -L 100000 >"+ccn_err_file
        ccn_p_2 = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,shell=True,start_new_session=True)
        try:
            pid_config.add_pid(str(ccn_p_2.pid), pid_file)
            for line in ccn_p_2.stdout:
                print(line)
        finally:
            ccn_p_2.terminate()
            ccn_p_2.wait()


if __name__ == "__main__" :
    stream_info = json.loads(util.base64todecode(sys.argv[1]))
    check()
