# -*- coding: utf-8 -*-
"""
celery 任务示例

本地启动celery命令: python  manage.py  celery  worker  --settings=settings
周期性任务还需要启动celery调度命令：python  manage.py  celerybeat --settings=settings
"""
import json
import datetime

from celery import task
from celery.schedules import crontab
from celery.task import periodic_task

from common.log import logger


