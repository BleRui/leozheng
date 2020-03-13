# -*- coding: utf-8 -*-
from django.db import models


# 创建表
class shopInfoTab(models.Model):
    username = models.CharField(max_length=20, default="")
    phone = models.CharField(max_length=30, default="")
    goods = models.CharField(max_length=50, default="")
    price = models.IntegerField(default=0)
    ordNum = models.CharField(max_length=50, default="")
