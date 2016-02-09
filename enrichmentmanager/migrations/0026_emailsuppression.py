# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('enrichmentmanager', '0025_auto_20151015_1618'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailSuppression',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('date', models.DateField(unique=True)),
            ],
        ),
    ]
