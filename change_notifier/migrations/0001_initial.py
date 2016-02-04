# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FamilyChangeNotification',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('last_run', models.DateTimeField()),
            ],
            options={
                'verbose_name': 'Family Change Notification Configuration',
            },
        ),
    ]
