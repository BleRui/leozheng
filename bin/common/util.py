#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import time
import unicodedata
import base64
import json
import os

def add_skip_path(skip_paths, stream_code_path,find_path, sub_path_list):
    if os.path.isdir(find_path):
        for item in os.listdir(find_path):
            if item == '.svn' or item == '.git':
                continue
            skip_item = os.path.join(find_path, item)
            if not os.path.isdir(skip_item):
                continue
            if not skip_item in ''.join(sub_path_list):
                skip_paths += ';.*'+skip_item.replace(stream_code_path, '')
            else:
                if not skip_item in sub_path_list:
                    skip_paths = add_skip_path(skip_paths, stream_code_path, skip_item, sub_path_list)
    return skip_paths
    
def get_datetime():
    return datetime.datetime.now().strftime('%Y-%m-%d_%H.%M.%S')

def compare(time1,time2):
    t1 = time.strptime(time1, '%Y-%m-%dT%H:%M:%S')
    t2 = time.strptime(time2, '%Y-%m-%dT%H:%M:%S')
    return t1 < t2
    
def is_number(num):
    try:
        float(num)
        return True
    except ValueError:
        pass
    
    try:
        unicodedata.numeric(num)
        return True
    except (TypeError, ValueError):
        pass
 
    return False

def GetMiddleStr(content,startStr,endStr):
  startIndex = content.find(startStr)
  if startIndex>=0:
    startIndex += len(startStr)
  endIndex = content.find(endStr)
  return content[startIndex:endIndex]
 
def base64toencode(content):
    return base64.b64encode(content).decode('utf-8')
  
def base64todecode(content):
    return base64.b64decode(content).decode("utf-8")

def str_to_bytes(content):
    return content.encode()

def bytes_to_str(content):
    return content.decode()
    
if __name__ == "__main__" :
    status = compare('2018-03-19T14:28:16','2018-03-19T14:28:16')
    print(status)