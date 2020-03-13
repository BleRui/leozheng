# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_application', '0008_workmanageinfotab_application_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workmanageinfotab',
            name='ScriptResults',
            field=models.CharField(default=b'', max_length=1200),
        ),
    ]
