# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('home_application', '0007_auto_20191207_1309'),
    ]

    operations = [
        migrations.AddField(
            model_name='workmanageinfotab',
            name='Application_time',
            field=models.DateTimeField(default=datetime.datetime(2019, 12, 9, 15, 22, 3, 69000), verbose_name=b'\xe6\x8f\x90\xe4\xba\xa4\xe6\x97\xb6\xe9\x97\xb4', auto_now_add=True),
            preserve_default=False,
        ),
    ]
