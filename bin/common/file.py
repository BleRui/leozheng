#!/usr/bin/python
# -*- coding: utf-8 -*-

import os,zipfile, re, tarfile
            
def delete_file_folder(src):
    '''delete files and folders''' 
    if os.path.isfile(src):  
        try:
            if os.path.islink(src):
                os.unlink(src)  
            else:
                os.remove(src)  
        except:  
            pass 
    elif os.path.isdir(src):  
        for item in os.listdir(src):  
            itemsrc=os.path.join(src,item)  
            delete_file_folder(itemsrc)  
        try:  
            if os.path.islink(src):
                os.unlink(src)  
            else:
                os.rmdir(src)  
        except:  
            pass
    else:
        try:  
            if os.path.islink(src):
                os.unlink(src)  
            else:
                os.rmdir(src)  
        except:  
            pass

def find_path_return_array(src, reg_path, str_array):
    if re.search('/'+reg_path+'$', src):
        #print("match paths: "+src)
        str_array.add(os.path.abspath(os.path.join(src, "..")))
    if os.path.isdir(src) and not '.svn' in src and not '.git' in src:  
        for item in os.listdir(src):  
            itemsrc=os.path.join(src,item)  
            find_path_return_array(itemsrc, reg_path, str_array)
    return str_array

def find_project_file_list_path(reg_path, project_file_list):
    with open(project_file_list, "r", encoding = 'utf-8') as list_file:
        lines=list_file.readlines()
        for line in lines:
            line = line.strip()
            if re.search(reg_path+'$', line.strip()):
                return line.strip()
    return ''
    
def find_path(src, reg_path):
    if re.search('/'+reg_path+'$', src):
        #print("match paths: "+src)
        return True
    if os.path.isdir(src) and not '.svn' in src and not '.git' in src:  
        for item in os.listdir(src):  
            itemsrc=os.path.join(src,item)  
            status = find_path(itemsrc, reg_path)
            if status == True:
                return status
    return False

def is_skip_path(src, reg_path):
    try:
        reg_path = reg_path.replace("+","_").replace('\\', '\\\\\\')
        src = src.replace("+","_")
        if re.search(reg_path, src):
            #print("match skip_paths: "+src)
            return True
    except:
        pass
    return False

def match_path(src, reg_path):
    reg_path = reg_path.replace("+","_").replace('\\', '\\\\\\')
    src = src.replace("+","_")
    if re.search(reg_path, src):
        return True
    return False
    
def unlink_file_folder(src):  
    if os.path.isfile(src):  
        try:
            if os.path.islink(src):
                os.unlink(src)  
        except:  
            pass 
    elif os.path.isdir(src):  
        for item in os.listdir(src):  
            itemsrc=os.path.join(src,item)  
            unlink_file_folder(itemsrc)  
        try:  
            if os.path.islink(src):
                os.unlink(src)  
        except:  
            pass  
        
def merge_intervals(intervals):
    """
    A simple algorithm can be used:
    1. Sort the intervals in increasing order
    2. Push the first interval on the stack
    3. Iterate through intervals and for each one compare current interval
    with the top of the stack and:
    A. If current interval does not overlap, push on to stack
    B. If current interval does overlap, merge both intervals in to one
        and push on to stack
    4. At the end return stack
    """
    si = sorted(intervals, key=lambda tup: tup[0], reverse=False)
    merged = []
    for tup in si:
        if not merged:
            merged.append(tup)
        else:
            b = merged.pop()
            if b[1] >= tup[0]:
                if b[1] >= tup[1]:
                    merged.append(b)
                else:
                    new_tup = tuple([b[0], tup[1]])
                    merged.append(new_tup)
            else:
                merged.append(b)
                merged.append(tup)
    return merged

def skip(stream_info):
    project_file_list = stream_info['PROJECT_FILE_LIST']
    root_path = stream_info['STREAM_CODE_PATH']
    # print("project file list: " + project_file_list)
    if os.path.isfile(project_file_list):
        os.remove(project_file_list)
    with open(project_file_list, "w", encoding = 'utf-8') as list_file:
        __walk(root_path, root_path, list_file, stream_info)        
  
def general_class_list_file(stream_info):
    project_class_file_list = stream_info['PROJECT_CLASS_FILE_LIST']
    root_path = stream_info['STREAM_CODE_PATH']
    stream_info["TARGET_SUBFIXS"] = 'class'
   #print("project class file list: " + project_class_file_list)
    if os.path.isfile(project_class_file_list):
        os.remove(project_class_file_list)
    with open(project_class_file_list, "w", encoding = 'utf-8') as list_file:
        __walk(root_path, root_path, list_file, stream_info) 

def __walk(root_path, path, list_file,stream_info):
    try:
        skip_paths_arrays = stream_info["SKIP_PATHS"].split(";")
        sub_code_path_list = ''
        if 'SUB_CODE_PATH_LIST' in stream_info and stream_info["SUB_CODE_PATH_LIST"] != '':
            sub_code_path_list = stream_info["SUB_CODE_PATH_LIST"].split(",")
        target_subfixs = stream_info["TARGET_SUBFIXS"].split(";")
        skip_target_subfixs = stream_info["SKIP_TARGET_SUBFIXS"].split(";")
        skip_items=stream_info["SKIP_ITEMS"].split(";")
        for item in os.listdir(path):
            if (item in skip_items):
                continue
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path) and not os.path.islink(item_path):
                for skip_path in skip_paths_arrays:
                    if skip_path != "" and is_skip_path(item_path, skip_path):
                        #print(stream_info['TOOL_TYPE']+" skip the paths :"+item_path+" "+skip_path)
                        break
                else:
                    __walk(root_path,item_path,list_file,stream_info)
            elif (item_path.rpartition('.')[2] in target_subfixs or "*" in target_subfixs) and not os.path.islink(item_path):
                for skip_subfixs in skip_target_subfixs:
                    if skip_subfixs != "" and re.search(skip_subfixs+"$", item_path):
                        break
                else:
                    for skip_path in skip_paths_arrays:
                            if skip_path != "" and is_skip_path(item_path, skip_path):
                                #print(stream_info['TOOL_TYPE']+" skip the paths :"+item_path)
                                break
                    else: 
                        match = False
                        if sub_code_path_list != '':
                            for skip_path in sub_code_path_list:
                                if skip_path != "" and match_path(item_path, skip_path):
                                    #print(stream_info['TOOL_TYPE']+" match the paths :"+item_path+" "+skip_path)
                                    match = True
                                    break
                        else:
                            match = True
                        if match:   
                            #print(stream_info['TOOL_TYPE']+ ' add file to list : ' + item_path)
                            list_file.write(item_path+"\n")
    except:
        pass
        
        
def unzip_file(zipfilename, unziptodir):
    if not os.path.exists(unziptodir): os.makedirs(unziptodir)
    sufix=os.path.splitext(zipfilename)[1]
    if sufix == ".zip":
        zfobj = zipfile.ZipFile(zipfilename)
        for name in zfobj.namelist():
            name = name.replace('\\','/')
            if name.endswith('/'):
                path1 = os.path.join(unziptodir, name)
                #print(path1)
                com=re.compile('/$')
                if not os.path.basename(com.sub('', path1)) == ".":
                    os.makedirs(path1)
            else:            
                ext_filename = os.path.join(unziptodir, name)
                ext_dir= os.path.dirname(ext_filename)
                if not os.path.exists(ext_dir) : os.makedirs(ext_dir)
                with open(ext_filename, 'wb') as outfile:
                    outfile.write(zfobj.read(name))
    elif sufix == ".gz":
        #print("loading the "+zipfilename+" data...")
        tar  = tarfile.open(zipfilename) 
        names = tar.getnames()   
        for name in names: 
            #print(name)
            tar.extract(name, unziptodir)  
        tar.close()  
