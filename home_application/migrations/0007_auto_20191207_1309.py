# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_application', '0006_workmanageinfotab_refusal_reasons'),
    ]

    operations = [
        migrations.AddField(
            model_name='workmanageinfotab',
            name='Applicant_display',
            field=models.CharField(default=b'', max_length=20),
        ),
        migrations.AddField(
            model_name='workmanageinfotab',
            name='Approver_display',
            field=models.CharField(default=b'', max_length=20),
        ),
        migrations.AddField(
            model_name='workmanagetab',
            name='Applicant_display',
            field=models.CharField(default=b'', max_length=20),
        ),
        migrations.AddField(
            model_name='workmanagetab',
            name='Approver_display',
            field=models.CharField(default=b'', max_length=20),
        ),
    ]
