# -*- coding: utf-8 -*-

from django.conf.urls import patterns

urlpatterns = patterns(
    'home_application.views',
    # 主页相关
    (r'^$', 'home'),
    (r'^login_info$', 'login_info'),
    (r'^get_allHost_ip$', 'get_allHost_ip'),
    (r'^get_allUser$', 'get_allUser'),
    (r'^get_work_management$', 'get_work_management'),
    (r'^add_save_wm$', 'add_save_wm'),
    (r'^delete_work_management$', 'delete_work_management'),
    (r'^modify_save_wm$', 'modify_save_wm'),
    (r'^submit$', 'submit'),
    (r'^Approval_pass$', 'Approval_pass'),
    (r'^add_submit$', 'add_submit'),
    (r'^refuse_fun$', 'refuse_fun'),
    (r'^delete_work_info$', 'delete_work_info'),
)
