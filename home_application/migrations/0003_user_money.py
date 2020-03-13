# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_application', '0002_user_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='money',
            field=models.IntegerField(default=0),
        ),
    ]
