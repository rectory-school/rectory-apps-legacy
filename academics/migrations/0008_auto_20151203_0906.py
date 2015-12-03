# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0007_auto_20151203_0903'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dorm',
            name='area',
        ),
        migrations.RemoveField(
            model_name='dorm',
            name='dorm',
        ),
        migrations.AddField(
            model_name='dorm',
            name='building',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dorm',
            name='level',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='dorm',
            name='wing',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
