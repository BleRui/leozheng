# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_application', '0010_remove_workmanagetab_applicant_display'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workmanageinfotab',
            name='Applicant_display',
        ),
    ]
