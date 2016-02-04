# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('change_notifier', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='familychangenotification',
            name='last_run',
            field=models.DateTimeField(null=True),
        ),
    ]
