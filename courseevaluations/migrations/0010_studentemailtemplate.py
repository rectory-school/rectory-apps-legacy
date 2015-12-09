# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courseevaluations', '0009_auto_20151209_1235'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentEmailTemplate',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('description', models.CharField(max_length=50)),
                ('subject', models.CharField(max_length=254)),
                ('template', models.TextField()),
                ('from_name', models.CharField(max_length=254)),
                ('from_address', models.EmailField(max_length=254)),
            ],
        ),
    ]
