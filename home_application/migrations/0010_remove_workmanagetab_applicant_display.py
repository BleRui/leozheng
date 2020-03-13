# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_application', '0009_auto_20191210_1215'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workmanagetab',
            name='Applicant_display',
        ),
    ]
