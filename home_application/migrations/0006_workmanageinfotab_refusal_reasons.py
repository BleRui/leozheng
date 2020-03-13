# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_application', '0005_workmanagetab_applicant'),
    ]

    operations = [
        migrations.AddField(
            model_name='workmanageinfotab',
            name='Refusal_reasons',
            field=models.CharField(default=b'', max_length=120),
        ),
    ]
