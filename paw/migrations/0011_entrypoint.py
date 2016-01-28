# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paw', '0010_auto_20160127_1349'),
    ]

    operations = [
        migrations.CreateModel(
            name='EntryPoint',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('domain', models.CharField(unique=True, max_length=254)),
                ('page', models.ForeignKey(to='paw.Page')),
            ],
        ),
    ]
