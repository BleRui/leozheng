# -*- coding: utf-8 -*-
from esb.client import EsbClient


def esb_get_biz(request=None):
    """获取蓝鲸业务"""
    return EsbClient(request).call('/api/c/compapi/v2/cc/search_business/', {}, 'post')


def esb_get_bk_template_by_biz(biz_id, request=None):
    return EsbClient(request).call('/api/c/compapi/v2/sops/get_template_list/',
                                   {'bk_biz_id': biz_id}, 'post')


def esb_get_param_by_template(temp_id, biz, request=None):
    return EsbClient(request).call('/api/c/compapi/v2/sops/get_template_info/',
                                   {'bk_biz_id': biz, 'template_id': temp_id}, 'get')


def esb_get_user(request=None):
    """获取蓝鲸用户"""
    return EsbClient(request).call('/api/c/compapi/v2/bk_login/get_all_users/', {}, 'get')


def esb_get_job_list(bk_biz_id, request=None):
    """获取业务下的作业模板"""
    return EsbClient(request).call('/api/c/compapi/v2/job/get_job_list/', {'bk_biz_id': bk_biz_id}, 'get')


def esb_get_job_detail(bk_biz_id, bk_job_id, request=None):
    """根据作业模板ID查询作业模板详情"""
    return EsbClient(request).call('/api/c/compapi/v2/job/get_job_detail/',
                                   {'bk_biz_id': bk_biz_id, 'bk_job_id': bk_job_id}, 'get')

