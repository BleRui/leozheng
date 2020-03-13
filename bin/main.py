#!/usr/bin/python
# -*- coding: utf-8 -*-
import platform,sys,os,subprocess
sys.path.append("./common/")
sys.path.append("./scm/")
sys.path.append("./tools_dep/")
import file,util,filter,ssh
import scm
import xml.etree.ElementTree as ET
import json
import datetime
import re
import codecc_web
import pid_config
import multiprocessing
import urllib.parse
import zlib,base64
import linecache
import result
import portalocker
import codecc_config as config
import time

def download_code(stream_info):    
    latest_info = ''
    try:
        #获取最近修改人, svn版本号, 修改时间
        if stream_info['SCM_TYPE'] != 'http_download' and stream_info['SCM_TYPE'] != 'code_download':
            latest_info = scm.print_revision_latest_time(stream_info)
        else:
            latest_info = stream_info["URL"]
    except Exception as e:
        raise Exception(e)
    return latest_info


def generate_data_json(stream_info):
    try:
        tool_type = stream_info['TOOL_TYPE']
        project_file_list=stream_info['PROJECT_FILE_LIST']
        if os.path.isfile(project_file_list):  
            with open(project_file_list, "r", encoding = 'utf-8') as file:
                generate_json_count=0
                process_generate_commit_json = multiprocessing.Pool(processes = int(stream_info['POOL_PROCESSES']))
                alllines = file.readlines()
                while (len(alllines) != 0):
                    for file_path_temp in alllines:
                        file_path=file_path_temp.strip()
                        alllines.remove(file_path_temp)
                        try:
                            generate_json_count+=1
                            process_generate_commit_json.apply_async(generate_file_data_json, (stream_info, file_path,))
                        except Exception as e:
                            print(e)
                                    
                process_generate_commit_json.close()
                process_generate_commit_json.join()
        #print(util.get_datetime()+" generate file count: "+str(generate_json_count))
    
    except Exception as e:
        raise Exception(e)
        
def generate_file_data_json(stream_info,file_path):
    try:
        tool_type = stream_info['TOOL_TYPE']
        filename_result=result.get_result_file_path(stream_info["STREAM_RESULT_PATH"],file_path)
        error_file = filename_result+".error"
        xml_file_path_url = filename_result+".scm_url.xml"
        xml_file_path_info = filename_result+".scm_info.xml"
        txt_file_path_blame = filename_result + ".scm_blame.txt"
        if not os.path.isfile(error_file) or not os.path.isfile(xml_file_path_info) or not os.path.isfile(txt_file_path_blame) or not os.path.isfile(xml_file_path_url):
            return
        
        error_lines = []
        blame_lines = []
        file_change_time = ""
        file_scm_info = {}
        filedata={}
        with open(error_file, "r", encoding = 'utf-8') as error_file_lines:
            error_lines = error_file_lines.readlines()
        with open(txt_file_path_blame, "r", encoding = 'utf-8') as blame_line:
            blame_lines = blame_line.readlines()
        file_change_time = scm.parse_info_xml(xml_file_path_info,stream_info)
        file_scm_info = scm.parse_log_xml(xml_file_path_url, file_path, stream_info)
        if len(error_lines) <= 0:
            return
        
        if tool_type == 'ccn':
            with open(stream_info['PROJECT_AVG_FILE_CC_LIST'], "a+", encoding = 'utf-8') as cc_file:
                portalocker.lock(cc_file, portalocker.LOCK_EX)
                cc_file.write(str(error_lines[len(error_lines)-1]))
        
        filedata["filename"] = file_path
        filedata["file_change_time"] = file_change_time
        if 'TOOL_TYPE' in stream_info:
            filedata["tool_name"] = stream_info['TOOL_TYPE']
        if 'TASK_ID' in stream_info:
            filedata["task_id"] = stream_info['TASK_ID']
        if 'STREAM_NAME' in stream_info:
            filedata["stream_name"] = stream_info['STREAM_NAME']
        if 'url' in file_scm_info:
            filedata["url"] = file_scm_info['url']
        if 'repo_id' in file_scm_info:
            filedata["repo_id"] = file_scm_info['repo_id']
        if 'revision' in file_scm_info:
            filedata["revision"] = file_scm_info['revision']
        if 'branch' in file_scm_info:
            filedata["branch"] = file_scm_info['branch']
        if 'rel_path' in file_scm_info:
            filedata["rel_path"] = file_scm_info['rel_path']
        if 'sub_module' in file_scm_info:
            filedata["sub_module"] = file_scm_info['sub_module']
        defects=[]

        if tool_type == "ccn":
            defects = defects_data_ccn(stream_info, error_lines, blame_lines)
        else:
            defects = defects_data(stream_info, error_lines, blame_lines)
        
        if len(defects) > 0:
            #压缩字符串
            zip_bytes = zlib.compress(bytes(json.dumps(defects), encoding='utf-8'))
            #base64编码
            zip_str = base64.b64encode(zip_bytes).decode('utf-8')
            filedata["defectsCompress"] = zip_str
            filedata_data = json.dumps(filedata)
            filedata_data = filedata_data.replace(": ", ":")
            #print(filedata_data)
            codecc_web.codecc_upload_file_json(filedata_data)
        #else:
        #    print(util.get_datetime()+" can not found defect file "+file_path)
    except Exception as e:
        raise Exception(e)
        
def defects_data(stream_info, error_lines, blame_lines):
    defects=[]
    try:
        for line in error_lines:
            defect={}
            line_array=line.strip().split("->")
            if len(line_array) >= 4:
                if line_array[1] == "0":line_array[1] = "1"
                defect["linenum"]=int(line_array[1])
                defect["category"]=line_array[2]
                defect["message"]=filter.message_filter(line_array[2], line_array[3], stream_info['TOOL_TYPE'],stream_info)
                if "goml" == stream_info['TOOL_TYPE']:
                    defect["linter"]=line_array[2]
                    if len(line_array) == 5:
                        defect["category"]=line_array[3]
                        defect["message"]=filter.message_filter(line_array[3], line_array[4], stream_info['TOOL_TYPE'],stream_info)
                if stream_info['SCM_TYPE'] != 'http_download':      
                    for sbl in blame_lines:
                        if re.search("^"+line_array[1]+"->", sbl):
                            sbl_array = sbl.strip().split("->")
                            defect["author"] = sbl_array[1]
                            temp_datetime = str(sbl_array[2]).split('.')[0]
                            st = time.strptime(temp_datetime, '%Y-%m-%dT%H:%M:%S')
                            defect["linenum_datetime"]  = int(round(time.mktime(st) * 1000))
                            break
                    else:
                        continue
                else:
                    defect["author"] = stream_info['PROJ_OWNER']
                defects.append(defect)
    except Exception as e:
        raise Exception(e)
        
    return defects

def defects_data_ccn(stream_info, error_lines, blame_lines):
    defects = []
    try:
        for idx, line in enumerate(error_lines):
            ccn_cc={}
            line_array=line.strip().split("->")
            if len(line_array) == 7:
                ccn_cc["function_name"]=line_array[1]
                ccn_cc["long_name"]=line_array[2]
                ccn_cc["total_lines"]=line_array[4]
                ccn_cc["ccn"]=line_array[5]
                ccn_cc["condition_lines"]=line_array[6].replace(' ', '').replace('{','').replace('}','')
                function_lines = line_array[3].split('-')
                ccn_cc["start_lines"]=function_lines[0]
                ccn_cc["end_lines"]=function_lines[1]
                author_info = ""
                for i in range(int(function_lines[0]),int(function_lines[1])):
                    line_blame_data = blame_lines[i].split('->')
                    if author_info != "":
                        info_array = author_info.split('->')
                        if util.compare(info_array[1].strip().split('.')[0],line_blame_data[2].strip().split('.')[0]):
                            author_info = line_blame_data[1]+"->"+line_blame_data[2].strip()
                    else:
                        author_info = line_blame_data[1]+"->"+line_blame_data[2].strip()
                ccn_cc["author"] = author_info.split('->')[0]
                temp_datetime = author_info.split('->')[1]
                st = time.strptime(temp_datetime, '%Y-%m-%dT%H:%M:%S.%f')
                final_datetime = time.mktime(st)
                ccn_cc["latest_datetime"] = int(round(final_datetime * 1000))
                defects.append(ccn_cc)
    except Exception as e:
        raise Exception(e)
        
    return defects
    
def dupc_generate_data_json(stream_info):
    try:
        all_result_json = {}
        with open(stream_info['PROJECT_FILE_DUPC_JSON'], "r", encoding = 'utf-8') as jsonfile:
            all_result_json = json.load(jsonfile)
            
        for idx, file_info in enumerate(all_result_json['files_info']):
            filedata={}
            filename_result = result.get_result_file_path(stream_info["STREAM_RESULT_PATH"], file_info['file_path'])
            txt_file_path_blame = filename_result + ".scm_blame.txt"
            xml_file_path_info = filename_result + ".scm_info.xml"
            xml_file_path_url = filename_result+".scm_url.xml"
            file_info["file_change_time"] = scm.parse_info_xml(xml_file_path_info,stream_info)
            filedata = scm.parse_log_xml(xml_file_path_url, file_info['file_path'], stream_info)
            blameline=""
            file_author_set = set([])
            if os.path.isfile(txt_file_path_blame):
                    with open(txt_file_path_blame, "r", encoding = 'utf-8') as blame_line:
                        blameline = blame_line.readlines()
            for block_idx, block in enumerate(file_info['block_list']):
                author_name_set = set([])
                author_name_list = []
                author_list = {}
                lines_list = range(0,len(blameline))
                
                if len(blameline) > int(block['start_lines']) and len(blameline) < int(block['end_lines']):
                    lines_list = range(int(block['start_lines']),len(blameline))
                    
                elif len(blameline) > int(block['end_lines']):
                    lines_list = range(int(block['start_lines']),int(block['end_lines']))
                    
                for i in lines_list:
                    line_blame_data = blameline[i].split('->')
                    author_name_list.append(line_blame_data[1])
                    author_name_set.add(line_blame_data[1])
                    if line_blame_data[1] in author_list:
                        change_time = author_list[line_blame_data[1]].strip().split('.')[0]
                        if util.compare(change_time,line_blame_data[2].strip().split('.')[0]):
                            author_list[line_blame_data[1]] = line_blame_data[2].strip()
                    else:
                        author_list[line_blame_data[1]] = line_blame_data[2].strip()
                author_info = ""
                for author_name in author_name_set:
                    if author_info != "":
                        info_array = author_info.split('->')
                        if int(info_array[1]) < author_name_list.count(author_name):
                            author_info = author_name+"->"+str(author_name_list.count(author_name))+"->"+author_list[author_name]
                    else:
                        author_info = author_name+"->"+str(author_name_list.count(author_name))+"->"+author_list[author_name]
                if author_info != "":
                    file_author_set.add(author_info.split('->')[0])
                    block['author'] = author_info.split('->')[0]
                    temp_datetime = str(author_info.split('->')[2])
                    st = time.strptime(temp_datetime, '%Y-%m-%dT%H:%M:%S.%f')
                    final_datetime = time.mktime(st)
                    block['latest_datetime'] = final_datetime
                file_info['block_list'][block_idx]  = block
            file_info['author_list'] = ';'.join(file_author_set)
            filedata['tool_name'] = 'dupc'
            filedata["stream_name"] = stream_info['STREAM_NAME']
            filedata["task_id"] = stream_info['TASK_ID']
            #压缩字符串
            zip_bytes = zlib.compress(bytes(json.dumps(file_info), encoding='utf-8'))
            #base64编码
            zip_str = base64.b64encode(zip_bytes).decode('utf-8')
            filedata["defectsCompress"] = zip_str
            filedata_data = json.dumps(filedata)
            filedata_data = filedata_data.replace(": ", ":")
            #print(util.get_datetime()+" start upload file "+file_info['file_path'])
           #print(filedata_data)
            codecc_web.codecc_upload_file_json(filedata_data)
        
        project_summary = {}
        project_summary['stream_name']  = stream_info['STREAM_NAME']
        project_summary['task_id'] = stream_info['TASK_ID']
        project_summary['scan_summary'] = all_result_json['scan_summary']
        summary_data = json.dumps(project_summary)
        summary_data = summary_data.replace(": ", ":")
        #print(util.get_datetime()+" start submit summary_data")
        codecc_web.upload_project_dupc_summary(summary_data)
    except Exception as e:
        raise Exception(e)
        
def main_scan(stream_info):
    try:
        if "SUB_PATH" in stream_info:
            os.environ["PATH"] = stream_info['SUB_PATH'] + os.pathsep + os.environ["PATH"]
        
        current_path=sys.path[0]
        tool_bin = os.path.join(current_path, 'tools')
        content = util.base64toencode(util.str_to_bytes(json.dumps(stream_info)))
        ex_py_script = ''
        
        if 'TOOL_TYPE' in stream_info:
            ex_py_script = stream_info['TOOL_TYPE'] +'_ext.py'   
            
        command = "python "+tool_bin + '/' + ex_py_script+" "+content
        print(util.get_datetime()+" start scan "+stream_info['TOOL_TYPE']+"...")
        proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,shell=True, start_new_session=True)
        pid_config.add_pid(str(proc.pid), stream_info["PID_FILE"])
        for line in proc.stdout:
            print(util.get_datetime()+" "+str(line))
        print(util.get_datetime()+" end scan "+stream_info['TOOL_TYPE'])    
    except Exception as e:
        raise Exception(e)
    finally:
        proc.terminate()
        proc.wait()
