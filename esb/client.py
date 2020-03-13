# -*- coding: utf-8 -*-
import json
import settings
import requests
try:
    from conf.default import DEFAULT_BK_API_VER
except ImportError:
    DEFAULT_BK_API_VER = 'v2'


class EsbClient:
    bk_token = ''

    def __init__(self, request=None):
        if request:
            self.bk_token = request.user.username

    def call(self, url, param, call_type, version=''):
        if not version:
            version = DEFAULT_BK_API_VER
        if version == 'v1':
            param['app_code'] = settings.APP_ID
            param['app_secret'] = settings.APP_TOKEN
            if self.bk_token:
                param['username'] = self.bk_token
        elif version == '' or version == 'v2':
            param['bk_app_code'] = settings.APP_ID
            param['bk_app_secret'] = settings.APP_TOKEN
            if self.bk_token:
                param['bk_username'] = self.bk_token
        else:
            return {'result': False, 'message': u'接口版本号"{0}"不存在'.format(version), "data": None}

        headers = {'Content-type': 'application/json'}
        url = "{0}{1}".format(settings.BK_PAAS_HOST, url)
        if call_type == 'post':
            res = requests.post(url=url, headers=headers, json=param, verify=False)
        else:
            res = requests.get(url=url, headers=headers, params=param, verify=False)
        result = json.loads(res.content)
        if result['result']:
            return result
        else:
            return {"result": False, "message": u"请求出现错误，错误状态：{0}".format(result["message"]), "data": None}
