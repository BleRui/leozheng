# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='shopInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(default=b'', max_length=20)),
                ('phone', models.CharField(default=b'', max_length=30)),
                ('goods', models.CharField(default=b'', max_length=50)),
                ('price', models.IntegerField(default=0)),
                ('ordNum', models.CharField(default=b'', max_length=50)),
            ],
        ),
    ]
