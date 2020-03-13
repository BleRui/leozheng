# -*- coding: utf-8 -*-
import sys

from common.mymako import render_mako_context, render_json
from conf.default import *
from home_application.models import *
import base64
import requests
import json
from django.db import transaction
import time
from django.db.models import Q

reload(sys)
sys.setdefaultencoding('utf8')

# 通用成功返回
SUCCESS_RETURN_DICT = {"result": True, "data": "success"}


def home(request):
    return render_mako_context(request, '/index.html')


def login_info(request):
    resp = render_json({
        "result": True,
        "data": {
            "username": request.user.username,
            "logout_url": LOGOUT_URL,
            "super": request.user.is_superuser
        }})
    from django.core.context_processors import csrf
    resp.set_cookie('cwcsrftoken', csrf(request)['csrf_token'])
    return resp


def get_allHost_ip(request):
    # 获取所有主机ip,并返回前端
    url = "http://paas.devtest.com/api/c/compapi/v2/cc/search_host/"
    headers = {"Accept": "application/json"}
    params = {
        "bk_app_code": "test",
        "bk_app_secret": "69965631-b22d-456f-bacf-05f5b720cb0e",
        "bk_username": "admin",
        "bk_biz_id": 2,
    }
    res = requests.post(url, json=params, headers=headers, verify=False)
    result = json.loads(res.content)
    tmp = result["data"]["info"]
    data = []
    for i in tmp:
        data.append(i["host"])
    return render_json({"result": True, "data": data})


def get_allUser(request):
    # 获取所有用户
    url = "http://paas.devtest.com/api/c/compapi/v2/usermanage/get_all_users/"
    headers = {"Accept": "application/json"}
    params = {
        "bk_app_code": "test",
        "bk_app_secret": "69965631-b22d-456f-bacf-05f5b720cb0e",
        "bk_username": "admin",
    }
    res = requests.post(url, json=params, headers=headers, verify=False)
    result = json.loads(res.content)
    return render_json({"result": True, "data": result["data"]})


def get_work_management(request):
    # 获取工单信息
    data = []
    data_Approval_info = []
    data_history_info = []
    res = workManageTab.objects.filter(Applicant=request.user.username)
    res_info = workManageInfoTab.objects.filter(Approver=request.user.username)
    res_info_history = workManageInfoTab.objects.filter(
        Q(Approver=request.user.username) | Q(Applicant=request.user.username))
    for i in res:
        data.append({
            "Job_title": i.Job_title,
            "Script_content": i.Script_content,
            "Approver": i.Approver,
            "Approver_display": i.Approver_display,
            "Job_content": i.Job_content,
            "Execution_host": i.Execution_host,
            "Applicant": i.Applicant,
            "id": i.id,
        })
    for i in res_info_history:
        data_history_info.append({
            "Job_title": i.Job_title,
            "Job_content": i.Job_content,
            "Execution_host": i.Execution_host,
            "Approver": i.Approver,
            "Approver_display": i.Approver_display,  # 审批人
            "Applicant": i.Applicant,
            "State": i.State,
            "Script_content": i.Script_content,
            "Application_time": i.Application_time,
            "ScriptResults": i.ScriptResults,
            "Refusal_reasons": i.Refusal_reasons,
            "id": i.id,
        })
    for i in res_info:
        if i.State == "审核中":
            data_Approval_info.append({
                "Job_title": i.Job_title,
                "Job_content": i.Job_content,
                "Execution_host": i.Execution_host,
                "Approver": i.Approver,
                "Approver_display": i.Approver_display,  # 审批人
                "Applicant": i.Applicant,
                "State": i.State,
                "Script_content": i.Script_content,
                "Application_time": i.Application_time,
                "id": i.id,
            })
    return render_json({"result": True, "data": data, "data_Approval_info": data_Approval_info,
                        "data_history_info": data_history_info})


def add_save_wm(request):
    # 添加工单
    params = json.loads(request.body)
    workManageTab.objects.create(
        Job_title=params["Job_title"],
        Job_content=params["Job_content"],
        Execution_host=params["Execution_host"],
        Script_content=params["Script_content"],
        Approver=params["Approver"],
        Approver_display=params["Approver_display"],
        Applicant=request.user.username
    )
    return render_json({"result": True})


def delete_work_management(request):
    # 删除一条工单
    params = json.loads(request.body)
    workManageTab.objects.filter(id=params["id"]).delete()
    return render_json({'result': True})


def modify_save_wm(request):
    # 工单管理_修改
    params = json.loads(request.body)
    workManageTab.objects.filter(id=params["id"]).update(
        Job_title=params["Job_title"],
        Job_content=params["Job_content"],
        Execution_host=params["Execution_host"],
        Script_content=params["Script_content"],
        Approver=params["Approver"],
        Approver_display=params["Approver_display"], )
    return render_json({'result': True})


def submit(request):
    # 工单管理_提交
    params = json.loads(request.body)
    res = workManageTab.objects.get(id=params["id"])
    with transaction.atomic():
        workManageTab.objects.filter(id=params["id"]).delete()
        workManageInfoTab.objects.create(
            Job_title=res.Job_title,
            Job_content=res.Job_content,
            Execution_host=res.Execution_host,
            Approver=res.Approver,
            Approver_display=res.Approver_display,  # 审批人
            Applicant=res.Applicant,
            State='审核中',
            Script_content=res.Script_content,
        )
    return render_json({'result': True})


def Approval_pass(request):
    # 审核通过
    params = json.loads(request.body)
    job_instance_id = fast_execute_script(params['Script_content'], params['Execution_host'])
    state = 100
    while state > 0:
        state -= 1
        result = get_job_instance_log(job_instance_id)
        if result:
            state = -1
    workManageInfoTab.objects.filter(id=params["id"]).update(State="通过", ScriptResults=result)
    return render_json({"result": True})


def add_submit(request):
    params = json.loads(request.body)
    print params
    workManageInfoTab.objects.create(
        Job_title=params["Job_title"],
        Job_content=params["Job_content"],
        Execution_host=params["Execution_host"],
        Approver=params["Approver"],
        Approver_display=params["Approver_display"],  # 审批人
        Applicant=request.user.username,
        State='审核中',
        Script_content=params["Script_content"],
    )
    return render_json({"result": True})


def refuse_fun(request):
    params = json.loads(request.body)
    print params
    workManageInfoTab.objects.filter(id=params["id"]).update(State=params["Status"],
                                                             Refusal_reasons=params["Refusal_reasons"])
    return render_json({"result": True})


def delete_work_info(request):
    params = json.loads(request.body)
    workManageInfoTab.objects.filter(id=params["id"]).delete()
    return render_json({'result': True})


def fast_execute_script(script_text, host_ip):
    # 快速执行脚本
    url = "http://paas.devtest.com/api/c/compapi/v2/job/fast_execute_script/"
    headers = {"Accept": "application/json"}
    script = script_text
    en_script = base64.b64encode(script)
    params = {
        "bk_app_code": "test",
        "bk_app_secret": "69965631-b22d-456f-bacf-05f5b720cb0e",
        "bk_username": "admin",
        "bk_biz_id": 2,
        "script_content": en_script,
        "account": "root",
        "script_type": "1",
        "ip_list": [
            {
                "bk_cloud_id": 0,
                "ip": host_ip
            }
        ]
    }
    # res = requests.get(url, params=params, headers=headers, verify=False)
    res = requests.post(url, json=params, headers=headers, verify=False)
    result = json.loads(res.content)
    return result["data"]["job_instance_id"]


def get_job_instance_log(job_instance_id):
    url = "http://paas.devtest.com/api/c/compapi/v2/job/get_job_instance_log/"
    headers = {"Accept": "application/json"}
    params = {
        "bk_app_code": "test",
        "bk_app_secret": "69965631-b22d-456f-bacf-05f5b720cb0e",
        "bk_username": "admin",
        "bk_biz_id": 2,
        "job_instance_id": job_instance_id
    }
    # res = requests.get(url, params=params, headers=headers, verify=False)
    res = requests.post(url, json=params, headers=headers, verify=False)
    result = json.loads(res.content)
    data = result["data"][0]["step_results"][0]["ip_logs"][0]["log_content"]
    return data

# def shopInfo(request):
#     # 获取数据库表
#     data = []
#     params = json.loads(request.body)
#     pageSize = params["pageSize"]
#     onPage = params["on_page"]
#
#     res = shopInfoTab.objects.all()
#     sizeAll = res.count()
#     # 分页计算获取数据
#     for i in range(0, sizeAll):
#         if (i >= pageSize * (onPage - 1)) and (i < pageSize * onPage):
#             data.append({
#                 "id": res[i].id,
#                 "username": res[i].username,
#                 "phone": res[i].phone,
#                 "goods": res[i].goods,
#                 "price": res[i].price,
#                 "ordNum": res[i].ordNum,
#             })
#     return render_json({"result": True, "data": data, "sizeAll": sizeAll})
#
#
# def addInfo(request):
#     # 添加
#     params = json.loads(request.body)
#     username1 = params["username"]
#     phone1 = params["phone"]
#     goods1 = params["goods"]
#     price1 = params["price"]
#     ordNum1 = params["ordNum"]
#     shopInfoTab.objects.create(username=username1, phone=phone1, goods=goods1, price=price1, ordNum=ordNum1)
#
#     res = shopInfoTab.objects.all()
#     data = getDataList(res)
#     return render_json({"result": True, "data": data})
#
#
# def removeInfo(request):
#     # 删除
#     params = json.loads(request.body)
#     id1 = params["id"]
#     shopInfoTab.objects.get(id=id1).delete()
#
#     res = shopInfoTab.objects.all()
#     data = getDataList(res)
#     return render_json({"result": True, "data": data})
#
#
# def editInfo(request):
#     # 修改
#     params = json.loads(request.body)
#     idEdit = params["id"]
#     usernameEdit = params["username"]
#     phoneEdit = params["phone"]
#     goodsEdit = params["goods"]
#     priceEdit = params["price"]
#     ordNumEdit = params["ordNum"]
#     shopInfoTab.objects.filter(id=idEdit).update(username=usernameEdit, phone=phoneEdit, goods=goodsEdit,
#                                                  price=priceEdit, ordNum=ordNumEdit)
#     res = shopInfoTab.objects.all()
#     data = getDataList(res)
#     return render_json({"result": True, "data": data})
#
#
# def searchText(request):
#     # 搜索
#     data = []
#     params = json.loads(request.body)
#     seText = params["seText"]
#     if seText == '':
#         res = ''
#     else:
#         getSeaText = shopInfoTab.objects.filter(username__contains=seText).values()
#         res = getSeaText[0]
#     return render_json({"result": True, "data": res})
