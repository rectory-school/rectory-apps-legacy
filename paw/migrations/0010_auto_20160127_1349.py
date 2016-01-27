# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paw', '0009_auto_20160127_1346'),
    ]

    operations = [
        migrations.AddField(
            model_name='textlink',
            name='page_link',
            field=models.ForeignKey(to='paw.Page', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='textlink',
            name='explicit_url',
            field=models.CharField(blank=True, max_length=4096),
        ),
    ]
