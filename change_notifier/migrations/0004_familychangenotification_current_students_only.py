# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('change_notifier', '0003_familychangenotification_users'),
    ]

    operations = [
        migrations.AddField(
            model_name='familychangenotification',
            name='current_students_only',
            field=models.BooleanField(default=True),
        ),
    ]
