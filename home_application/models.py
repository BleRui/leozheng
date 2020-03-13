# -*- coding: utf-8 -*-
from django.db import models


class workManageTab(models.Model):
    # 未提交的工单管理表
    Job_title = models.CharField(max_length=30, default="")
    Job_content = models.CharField(max_length=50, default="")
    Execution_host = models.CharField(max_length=30, default="")
    Script_content = models.CharField(max_length=120, default="")
    Approver = models.CharField(max_length=20, default="")
    Approver_display = models.CharField(max_length=20, default="")  # 审批人
    Applicant = models.CharField(max_length=20, default="")


class workManageInfoTab(models.Model):
    # 已提交的工单管理信息表
    Job_title = models.CharField(max_length=30, default="")
    Job_content = models.CharField(max_length=50, default="")
    Execution_host = models.CharField(max_length=30, default="")
    Approver = models.CharField(max_length=20, default="")
    Application_time=models.DateTimeField("提交时间",auto_now_add=True)
    Approver_display = models.CharField(max_length=20, default="")  # 审批人
    Applicant = models.CharField(max_length=20, default="")
    State = models.CharField(max_length=20, default="")
    Script_content = models.CharField(max_length=120, default="")
    ScriptResults = models.CharField(max_length=1200, default="")
    Refusal_reasons = models.CharField(max_length=120, default="")
