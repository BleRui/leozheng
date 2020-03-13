# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_application', '0002_auto_20191130_1957'),
    ]

    operations = [
        migrations.DeleteModel(
            name='shopInfoTab',
        ),
    ]
