# -*- coding: utf-8 -*-
import sys
import requests
import base64en

from common.mymako import render_mako_context, render_json
from conf.default import *
from home_application.models import *
from django.db import transaction  # 引入transaction 将代码放入一个事务
from django.db.models import F  # 引入F ，将数据库的一个值取出来
import json
from common.log import logger
from home_application.celery_tasks import *

reload(sys)
sys.setdefaultencoding('utf8')

# 通用成功返回
SUCCESS_RETURN_DICT = {"result": True, "data": "success"}


def home(request):
    # url = "http://paas.devtest.com/api/c/compapi/v2/cc/search_business/"
    # headers = {"Accept": "application/json"}
    # params = {
    #     "bk_app_code": "test",
    #     "bk_app_secret": "69965631-b22d-456f-bacf-05f5b720cb0e",
    #     "bk_username": "admin",
    # }
    #
    # # res = requests.get(url, params=params, headers=headers, verify=False)
    # res = requests.post(url, json=params, headers=headers, verify=False)
    # result = json.loads(res.content)
    # print result
    a = base64en.b64encode("hostname")
    print a
    print request.user.username
    print request.user.is_superuser
    print request.COOKIES.get('bk_token')
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


def test(request):
    # searchUser()
    # deleteUser()
    # pay()
    # addComputer()
    # deleteComputer()
    # try:
    #     a=1+'e'
    # except Exception as e:
    #     logger.error(e)
    # celery_test.delay()
    # celery_async.apply_async(eta=datetime.datetime.now() +
    #                              datetime.timedelta(seconds=20))
    # print 2
    res=User.objects.get(username='kahuf')
    print res.money
    return render_json({"result": True, "data": "sucess"})


def addUser(request):
    User.objects.create(username='zheng', age=11, sex=True, phone='188')
    return render_json({"result": True})


def updateUser():
    User.objects.filter(id=1).update(phone="200")
    obj = User.objects.get(id=1)
    obj.username = "liang"
    obj.save()


def searchUser():
    # obj=User.objects.all()
    # res=User.objects.filter(username__contains="li").values()[0]["username"]
    # res=User.objects.filter(id=1).count()#统计
    # is_exist=User.objects.exists()#排除id=1或者（）表示非空
    # User.objects.all().order_by('id') #排序
    # return render_json(res)
    # obj=User.objects.get(username="user6")
    # obj1 = UserInfo.objects.get(user_id=obj.id)
    # print obj1.id_card
    #
    # print User.objects.get(username="user6").userinfo.id_card
    # print UserInfo.objects.get(id_card__contains="12").user.username
    # 查找一对多
    # obj1=User.objects.get(username='liang')
    # print Computer.objects.get(user_id=obj1.id).name
    # for j in Computer.objects.filter(user_id=obj1.id).values():
    #     print j["name"]
    # obj2=Computer.objects.filter(name='E').values()
    # print User.objects.get(id=obj2[0]["user_id"]).username
    # 使用_set查找一对多的方法
    obj1 = User.objects.get(username="liang").computer_set.all()
    for j in obj1:
        print j.name


def deleteUser():
    User.objects.filter(username="test").delete()


def pay():
    # print a
    #     # print b
    #     # User.objects.filter(id=1).update(money=a-50)
    #     # User.objects.filter(id=2).update(money=b+50)
    with transaction.atomic():  # 事务中，要讲所有代码运行成功才执行
        #     a = User.objects.get(id=1)
        #     a.money -= 50
        #     a.save()
        #
        #     a = 1 + 'str'
        #
        #     b = User.objects.get(id=2)
        #     b.money += 50
        #     b.save()

        User.objects.filter(id=1).update(money=F('money') - 50)  # 直接取出来加50
        User.objects.filter(id=2).update(money=F('money') + 50)  # 直接取出来减50


def addComputer():
    userObj = User.objects.get(id=1)
    # 三种方式添加相关联的值
    Computer.objects.create(name='E', user=userObj)  # 将整个对象传进去
    Computer.objects.create(name='F', user_id=userObj.id)
    userObj.computer_set.create(name='o', price=10000)  # 相关联的表创建


def deleteComputer():
    obj1 = User.objects.get(id=1).computer_set.all()
    for i in obj1:
        i.delete()

    obj2 = User.objects.get(username='liang')
    obj2.computer_set2


def addBookUser():
    # userObj=User.objects.get(id=1)
    # userObj.books_set.create(name="lalla",price=100)
    # userObj.books_set.create(name="lia1", price=100)
    # bookObj=books.objects.get(id=2)
    # bookObj.User_se
    userObj = User.objects.get(id=1)
    userObj2 = User.objects.get(id=2)
    bookObj = Books.objects.get(id=1)
    bookObj2 = Books.objects.get(id=2)
    userObj.books_set.add(bookObj)
    userObj.books_set.add(bookObj2)
    bookObj2.user.add(userObj)
    bookObj2.user.add(userObj2)
    userObj.save()
    bookObj2.save()


def get_user_info(request):
    num1 = request.GET.get("num1", '')
    num2 = request.GET.get("num2", '')
    res_num = int(num1) + int(num2)
    res = User.objects.all()
    data = []
    for i in res:
        data.append({
            "name": i.username,
            "age": i.age
        })
    return render_json({"result": True, "data": data, "res_num": res_num})


def addnum(request):
    params = json.loads(request.body)
    num1 = params["num1"]
    num2 = params["num2"]
    res_num = int(num1) + int(num2)
    return render_json({"result": True, "res_num": res_num})
