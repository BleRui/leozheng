# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_application', '0003_delete_shopinfotab'),
    ]

    operations = [
        migrations.CreateModel(
            name='workManageInfoTab',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Job_title', models.CharField(default=b'', max_length=30)),
                ('Job_content', models.CharField(default=b'', max_length=50)),
                ('Execution_host', models.CharField(default=b'', max_length=30)),
                ('Applicant', models.CharField(default=b'', max_length=20)),
                ('Approver', models.CharField(default=b'', max_length=20)),
                ('State', models.CharField(default=b'', max_length=20)),
                ('Script_content', models.CharField(default=b'', max_length=120)),
                ('ScriptResults', models.CharField(default=b'', max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='workManageTab',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Job_title', models.CharField(default=b'', max_length=30)),
                ('Job_content', models.CharField(default=b'', max_length=50)),
                ('Execution_host', models.CharField(default=b'', max_length=30)),
                ('Script_content', models.CharField(default=b'', max_length=120)),
                ('Approver', models.CharField(default=b'', max_length=20)),
            ],
        ),
    ]
