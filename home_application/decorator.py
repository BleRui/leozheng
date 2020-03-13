# -*- coding: utf-8 -*-
from common.log import logger
from common.mymako import render_json


def api_try_except(func):
    """视图函数异常捕捉装饰器"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.exception(e.message)
            return render_json({"result": False, "data": [u"系统异常，请联系管理员！"]})
    return wrapper


def log_request_params(func):
    """视图函数参数记录装饰器"""
    def wrapper(request, *args, **kwargs):
        if request.method == "GET":
            logger.debug("request method: GET, params: \n %s" % request.GET)
        elif request.method == "POST":
            logger.debug("request method: POST, params: \n %s" % request.body)
        return func(request, *args, **kwargs)
    return wrapper