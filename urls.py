# -*- coding: utf-8 -*-

from django.conf.urls import patterns

urlpatterns = patterns(
    'home_application.views',
    # 主页相关
    (r'^$', 'home'),
    (r'^login_info$', 'login_info'),
    (r'^test$', 'test'),
    (r'^shopInfo$', 'shopInfo'),
    (r'^addInfo$', 'addInfo'),
    (r'^editInfo$', 'editInfo'),
    (r'^removeInfo$', 'removeInfo'),
    (r'^searchText$', 'searchText')
)
