# -*- coding: utf-8 -*-
import sys

from common.mymako import render_mako_context, render_json
from conf.default import *
from home_application.models import *
import json

reload(sys)
sys.setdefaultencoding('utf8')

# 通用成功返回
SUCCESS_RETURN_DICT = {"result": True, "data": "success"}


def home(request):
    return render_mako_context(request, '/index.html')


# def login_info(request):
#     resp = render_json({
#         "result": True,
#         "data": {
#             "username": request.user.username,
#             "logout_url": LOGOUT_URL,
#             "super": request.user.is_superuser
#         }})
#     from django.core.context_processors import csrf
#     resp.set_cookie('cwcsrftoken', csrf(request)['csrf_token'])
#     return resp


def getDataList(res):
    data = []
    for i in res:
        data.append({
            "id": i.id,
            "username": i.username,
            "phone": i.phone,
            "goods": i.goods,
            "price": i.price,
            "ordNum": i.ordNum
        })
    return data


def shopInfo(request):
    # 获取数据库表
    data = []
    params = json.loads(request.body)
    pageSize = params["pageSize"]
    onPage = params["on_page"]

    res = shopInfoTab.objects.all()
    sizeAll = res.count()
    # 分页计算获取数据
    for i in range(0, sizeAll):
        if (i >= pageSize * (onPage - 1)) and (i < pageSize * onPage):
            data.append({
                "id": res[i].id,
                "username": res[i].username,
                "phone": res[i].phone,
                "goods": res[i].goods,
                "price": res[i].price,
                "ordNum": res[i].ordNum,
            })
    return render_json({"result": True, "data": data, "sizeAll": sizeAll})


def addInfo(request):
    # 添加
    params = json.loads(request.body)
    username1 = params["username"]
    phone1 = params["phone"]
    goods1 = params["goods"]
    price1 = params["price"]
    ordNum1 = params["ordNum"]
    shopInfoTab.objects.create(username=username1, phone=phone1, goods=goods1, price=price1, ordNum=ordNum1)

    res = shopInfoTab.objects.all()
    data = getDataList(res)
    return render_json({"result": True, "data": data})


def removeInfo(request):
    # 删除
    params = json.loads(request.body)
    id1 = params["id"]
    shopInfoTab.objects.get(id=id1).delete()

    res = shopInfoTab.objects.all()
    data = getDataList(res)
    return render_json({"result": True, "data": data})


def editInfo(request):
    # 修改
    params = json.loads(request.body)
    idEdit = params["id"]
    usernameEdit = params["username"]
    phoneEdit = params["phone"]
    goodsEdit = params["goods"]
    priceEdit = params["price"]
    ordNumEdit = params["ordNum"]
    shopInfoTab.objects.filter(id=idEdit).update(username=usernameEdit, phone=phoneEdit, goods=goodsEdit,
                                                 price=priceEdit, ordNum=ordNumEdit)
    res = shopInfoTab.objects.all()
    data = getDataList(res)
    return render_json({"result": True, "data": data})


def searchText(request):
    # 搜索
    data = []
    params = json.loads(request.body)
    seText = params["seText"]
    if seText == '':
        res = ''
    else:
        getSeaText = shopInfoTab.objects.filter(username__contains=seText).values()
        res = getSeaText[0]
    return render_json({"result": True, "data": res})
