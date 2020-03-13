#!/usr/bin/python
# -*- coding: utf-8 -*-
import socket

def get_local_ip(): 
    localIP = socket.gethostbyname(socket.gethostname())
    return "%s "%localIP
    
def get_host_ip():
    host_ip = ""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        host_ip = s.getsockname()[0]
    except Exception:
        return "get host ip failed!"
    finally:
        s.close()
    return host_ip
    
def telnet_upload_server(ip, port):
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sk.settimeout(1)
    try:
        sk.connect((ip , int(port)))
        return True
    except Exception:
        return False
    finally:
        sk.close()
    