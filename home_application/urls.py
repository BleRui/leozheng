# -*- coding: utf-8 -*-

from django.conf.urls import patterns

urlpatterns = patterns(
    'home_application.views',
    # 主页相关
    (r'^$', 'home'),
    (r'^login_info$', 'login_info'),
    (r'^test$', 'test'),
    (r'^addUser$','addUser'),
    (r'^get_user_info', 'get_user_info'),
    (r'^addnum', 'addnum')
)
