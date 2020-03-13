# -*- coding: utf-8 -*-
"""
celery 任务示例

本地启动celery命令: python  manage.py  celery  worker  --settings=settings
周期性任务还需要启动celery调度命令：python  manage.py  celerybeat --settings=settings
"""
import json
import datetime
import time

from celery import task
from celery.schedules import crontab
from celery.task import periodic_task

from common.log import logger


@task
def celery_test():
    print 'sleep 2 seconds'
    time.sleep(3)
    print 1


@task
def celery_async():
    print "liang"


@periodic_task(run_every=crontab(minute="*/1", hour="*",
                                 day_of_week="*"))
def celery_periodic():
    print 1
