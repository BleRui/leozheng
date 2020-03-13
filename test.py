# -*- coding: utf-8 -*-
import json
import requests

def crete():
    url = 'http://paas.canway.club/api/c/compapi/v2/sops/create_task/'
    param = {
        'bk_app_code':'linuxcheck',
        'bk_app_secret':'5c428d5e-334b-11e9-a2b5-dc5360b53bd1',
        'bk_username':'admin',
        'bk_biz_id':'2',
        'template_id':'1',
        'name':'123123',
    }
    headers = {'Content-type': 'application/json'}
    res = requests.post(url=url, headers=headers, json=param,verify=False)
    print json.loads(res.content)

def run():
    url = 'http://paas.canway.club/api/c/compapi/v2/sops/operate_task/'
    param = {
        'bk_app_code':'linuxcheck',
        'bk_app_secret':'5c428d5e-334b-11e9-a2b5-dc5360b53bd1',
        'bk_username':'admin',
        'bk_biz_id':'2',
        'task_id':'9',
        'action':'start',
    }
    headers = {'Content-type': 'application/json'}
    res = requests.post(url=url, headers=headers, json=param,verify=False)
    print json.loads(res.content)

def get():
    url = 'http://paas.canway.club/api/c/compapi/v2/sops/get_task_status/'
    param = {
        'bk_app_code': 'linuxcheck',
        'bk_app_secret': '5c428d5e-334b-11e9-a2b5-dc5360b53bd1',
        'bk_username': 'admin',
        'bk_biz_id': '2',
        'task_id': '9',
    }
    headers = {'Content-type': 'application/json'}
    res = requests.post(url=url, headers=headers, json=param, verify=False)
    print json.loads(res.content)

def operate():
    url = 'http://paas.canway.club/api/c/compapi/v2/sops/operate_task/'
    param = {
        'bk_app_code': 'linuxcheck',
        'bk_app_secret': '5c428d5e-334b-11e9-a2b5-dc5360b53bd1',
        'bk_username': 'admin',
        'bk_biz_id': '2',
        'task_id': '55',
        'action': 'pause',
    }
    headers = {'Content-type': 'application/json'}
    res = requests.post(url=url, headers=headers, json=param, verify=False)
    print json.loads(res.content)
operate()

