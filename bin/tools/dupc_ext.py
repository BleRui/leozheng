import sys
sys.path.append("../common/")
import codecs
import file
import hashlib
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
    stream_code_path = ""
    project_dupc_xml = ""
    pool_processes = ""
    pid_file = ""
    skip_paths_arg = ""
    suffix_list = []
    
    if 'STREAM_CODE_PATH' in stream_info:
        stream_code_path = stream_info['STREAM_CODE_PATH']
    if 'PROJECT_DUPC_XML' in stream_info:
        project_dupc_xml = stream_info['PROJECT_DUPC_XML']
    if 'POOL_PROCESSES' in stream_info:
        pool_processes = stream_info['POOL_PROCESSES']
    if 'PID_FILE' in stream_info:
        pid_file = stream_info['PID_FILE']
    if 'TARGET_SUBFIXS' in stream_info:
        suffix_list = stream_info['TARGET_SUBFIXS'].split(';')
    
    if 'SUB_CODE_PATH_LIST' in stream_info and stream_info['SUB_CODE_PATH_LIST'] != '':
        sub_code_path_list = stream_info['SUB_CODE_PATH_LIST'].split(',')
        sub_path_list = [''.join(stream_code_path+'/'+path).replace('//','/') for path in sub_code_path_list]
        find_path = stream_code_path
        stream_info['SKIP_PATHS'] += util.add_skip_path('', stream_code_path, find_path, sub_path_list)
        
    if 'SKIP_PATHS' in stream_info:
        skip_path_list = stream_info['SKIP_PATHS'].split(';')
        skip_paths_arg = get_skip_paths_arg(stream_code_path, skip_path_list)

    if stream_code_path == '' or project_dupc_xml == '' or pool_processes == '' or pid_file == '':
        print('below option is empty!')
        print('stream_code_path: '+stream_code_path)
        print('project_dupc_xml: '+project_dupc_xml)
        print('pool_processes: '+pool_processes)
        print('pid_file: '+pid_file)
        exit(1)
                
    current_path=sys.path[0]+'/../'
    dupc_tool_path = os.path.join(current_path, 'tools_dep/dupc/bin/run.sh')
    os.chmod(dupc_tool_path, 0o755)
    

    #print('scaning...')
    suffix_list = map_suffix_list(suffix_list)
    language_xml_list = []
    print(suffix_list)
    for suffix in suffix_list:
        command = dupc_tool_path+" cpd "+"--minimum-tokens 100 --format xml --encoding utf-8 "+ \
            " --files "+stream_code_path+" --language "+suffix+" --skip-lexical-errors"+skip_paths_arg +" 2>/dev/null"
        dupc_p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True, start_new_session=True)
        try:
            pid_config.add_pid(str(dupc_p.pid), pid_file)
            xml_suffix = "_" + suffix + ".xml"
            language_dupc_xml = project_dupc_xml.replace(".xml", xml_suffix)
            with open(language_dupc_xml, "a+", encoding = 'utf-8') as file:
                is_codefrag = False
                codefrag = ""
                indent = ""
                for line in dupc_p.stdout:
                    line_str = str(line.decode("utf-8"))
                    #不再将codefragment写入xml，用md5对codefragment转换为fingerprint写入
                    if "<codefragment>" in line_str and "</codefragment>" in line_str:
                        is_codefrag = False
                        codefrag = ""
                        indent = re.search(".*(?=<codefragment)", line_str).group(0)
                        finger_print = indent + "<fingerprint>" + get_md5(line_str) + "</fingerprint>\n"
                        file.write(finger_print)
                    elif "<codefragment>" in line_str:
                        is_codefrag = True
                        codefrag += line_str
                        indent = re.search(".*(?=<codefragment)", line_str).group(0)
                    elif "</codefragment>" in line_str:
                        is_codefrag = False
                        codefrag += line_str
                        finger_print = indent + "<fingerprint>" + get_md5(codefrag) + "</fingerprint>\n"
                        codefrag = ""
                        indent = ""
                        file.write(finger_print)
                    else:
                        if is_codefrag:
                            codefrag += line_str
                        else:
                            file.write(line_str)
            language_xml_list.append(language_dupc_xml)
        finally:
            dupc_p.terminate()
            dupc_p.wait()
    
    os.chdir(current_path)

    merge_language_xml_files(project_dupc_xml, language_xml_list)

    parse_project_dupc_xml_file_list(project_dupc_xml, stream_info['PROJECT_FILE_LIST'])
    
    parse_project_dupc_xml_to_json(project_dupc_xml, stream_info['PROJECT_FILE_DUPC_JSON'])

def merge_language_xml_files(project_dupc_xml, language_xml_list):
    try:
        root = ET.Element("pmd-cpd")
        for language_dupc_xml in language_xml_list:
            if os.path.isfile(language_dupc_xml):
                sub_root = ET.ElementTree(file=language_dupc_xml).getroot()
                for elem in sub_root.findall("duplication"):
                    root.append(elem)
        tree = ET.ElementTree(root)
        tree.write(project_dupc_xml, "utf-8")
    except Exception as e:
        print('=>dupc_ext.py->merge_language_xml_files->ERROR:'+str(e)+":"+project_dupc_xml)

def get_skip_paths_arg(target_path, skip_path_list):
    skip_paths_arg = ""        
    if not os.path.isdir(target_path):
        return skip_paths_arg
    for item in os.listdir(target_path):
        if item == '.svn' or item == '.git':
            continue
        item_path = os.path.join(target_path, item)
        if os.path.isdir(item_path):
            item_path += "/"
        elif os.path.isfile(item_path):
            #do nothing
            pass
        else:
            continue
        for skip_path in skip_path_list:
            if skip_path.replace(' ', '') == "":
                continue
            try:
                re.compile(skip_path) #判断是否有效正则
            except re.error:
                continue
            if re.search(skip_path, item_path):
                skip_paths_arg += " --exclude " + item_path
                break
        else:
            skip_paths_arg += get_skip_paths_arg(item_path, skip_path_list)
    return skip_paths_arg

def parse_project_dupc_xml_file_list(project_dupc_xml, project_file_list):
    sort_file_paths=set([])
    if os.path.isfile(project_dupc_xml):
        try:
            tree = ET.ElementTree(file=project_dupc_xml)
            for elem in tree.iter("file"):
                source_file = elem.attrib['path']
                sort_file_paths.add(source_file)
        except Exception as e:
            print('=>dupc_ext.py->parse_project_dupc_xml_file_list->ERROR:'+str(e)+":"+project_dupc_xml)

    with open(project_file_list, "a+", encoding = 'utf-8') as file_list:
        for sourcefile in sort_file_paths:
            file_list.write(sourcefile+"\n")
    
def parse_project_dupc_xml_to_json(project_dupc_xml, project_file_dupc_json):
    all_result_json = {}
    files_info = []
    scan_result = []
    scan_summary = {}
    sort_file_paths=set([])
    file_paths=[]
    all_dupfilelines={}
    dup_line_count=0
    files_total_lines = 0
    if os.path.isfile(project_dupc_xml):
        tree = ET.ElementTree(file=project_dupc_xml)
        for elem in tree.iter("duplication"):
            finger_print = elem.find("fingerprint").text
            dup_block={}
            block_list = []
            for sub_elem in elem.iter(): 
                if "file" == sub_elem.tag:
                    source_file = sub_elem.attrib['path']
                    start_line = sub_elem.attrib['line']
                    end_line = sub_elem.attrib['end_line']
                    dup_block['finger_print'] = finger_print
                    block_list.append({'source_file': source_file, 'start_lines': start_line, 'end_lines': end_line})
                    sort_file_paths.add(source_file)
                    file_paths.append(source_file)
                    if source_file in all_dupfilelines:
                        all_dupfilelines[source_file] += ";"+start_line+"-"+end_line+"-"+finger_print
                    else:
                        all_dupfilelines[source_file] = start_line+"-"+end_line+"-"+finger_print
            dup_block['block_list'] = block_list
            scan_result.append(dup_block)
    
    for sourcefile in sort_file_paths:
        file_block_list = []
        dup_file={}
        
        dup_file['file_path'] = sourcefile
        dup_file['block_num'] = file_paths.count(sourcefile)
        dup_file_info = sourcefile
        dup_file_info += "->"+str(file_paths.count(sourcefile))
        file_lines_intervals = []
        dup_line_number = 0
        line_array = all_dupfilelines[sourcefile].split(";")
        for start_end_line in line_array:
            line_rang = start_end_line.split("-")
            file_lines_intervals.append((int(line_rang[0]),int(line_rang[1])))
            file_block_list.append({'start_lines': int(line_rang[0]), 'end_lines': int(line_rang[1]), 'finger_print' : line_rang[2]})
        file_merge_lines_intervals = file.merge_intervals(file_lines_intervals)
        for rang in file_merge_lines_intervals:
            dup_line_number += int(rang[1]) - int(rang[0]) + 1
        dup_file['dup_lines'] = dup_line_number
        dup_line_count += dup_line_number
        dup_file_info += "->"+str(dup_line_number)
        if os.path.isfile(sourcefile):
            with open(sourcefile, "rb") as code_file:
                data = code_file.read()
                data = str(data).replace('\\r\\n','\\n').replace('\\r','\\n')
                data_array = str(data).split('\\n')
                lines = len(data_array)
                dup_file['total_lines'] = lines
                files_total_lines += lines
            dup_file_info += "->"+str(lines)
            if lines > 0:
                dup_file['dup_rate'] = '{:.2f}'.format(float(dup_line_number / lines *100))+'%'
                dup_file_info += "->"+'{:.2f}'.format(float(dup_line_number / lines *100))+'%'
        if len(file_block_list) > 0:
            dup_file['block_list'] = file_block_list
        files_info.append(dup_file)
    
    scan_summary['rawline_count'] = files_total_lines
    scan_summary['dup_line_count'] = dup_line_count
    all_result_json['files_info'] = files_info
    all_result_json['scan_summary'] = scan_summary
    with open(project_file_dupc_json, "w", encoding = 'utf-8') as dupc_json:
        dupc_json.write(json.dumps(all_result_json))

def map_language(language_suffix):
    lang_map = {
        "cs" : "cs",
        "c" : "cpp",
        "cc" : "cpp",
        "cpp" : "cpp",
        "cxx" : "cpp",
        "h" : "cpp",
        "hh" : "cpp",
        "hpp" : "cpp",
        "hxx" : "cpp",
        "java" : "java",
        "php" : "php",
        "mm" : "objectivec",
        "m" : "objectivec",
        "py" : "python",
        "js" : "ecmascript",
        "rb" : "ruby",
        "go" : "go",
        "swift" : "swift",
        "kt" : "kotlin"
    }
    return lang_map.get(language_suffix, None)

def map_suffix_list(suffix_list):
    new_list = []
    for suffix in suffix_list:
        language = map_language(suffix)
        if not language == None and not language in new_list:
            new_list.append(language)
    return new_list

def get_md5(code_fragment):
    md5_obj = hashlib.md5()
    md5_obj.update(code_fragment.encode(encoding='utf-8'))
    md5 = md5_obj.hexdigest() #生成md5
    return md5

if __name__ == "__main__" :
    stream_info = json.loads(util.base64todecode(sys.argv[1]))
    check()
