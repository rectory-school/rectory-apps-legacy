# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0024_grade_school'),
    ]

    operations = [
        migrations.CreateModel(
            name='Parent',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('family_id', models.CharField(max_length=20)),
                ('parent_id', models.CharField(max_length=2)),
                ('full_id', models.CharField(max_length=22, unique=True)),
                ('first_name', models.CharField(max_length=50, blank=True)),
                ('last_name', models.CharField(max_length=50, blank=True)),
                ('email', models.EmailField(max_length=254, blank=True)),
                ('phone_home', models.CharField(max_length=20, blank=True)),
                ('phone_work', models.CharField(max_length=20, blank=True)),
                ('phone_cell', models.CharField(max_length=20, blank=True)),
            ],
        ),
    ]
