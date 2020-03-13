# -*- coding: utf-8 -*-
from django.db import models


class User(models.Model):
    username = models.CharField(max_length=20, default=u"未知")
    age = models.IntegerField()
    sex = models.BooleanField()
    phone = models.CharField(max_length=30, default=b"")
    money = models.IntegerField(default=0)


class UserInfo(models.Model):  # 创建UserInfo表
    id_card = models.CharField(default="", max_length=30)
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)  # 创建一个字段与User表相关联，级联删除


class Computer(models.Model):
    name = models.CharField(max_length=40, default='')
    price = models.IntegerField(default=5000)
    user = models.ForeignKey(to=User)  # 多对一，要写在多的里面


class Books(models.Model):
    name = models.CharField(max_length=50, default='')
    price = models.IntegerField(default=100)
    user = models.ManyToManyField(User)
