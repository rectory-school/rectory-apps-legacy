# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0010_auto_20151203_0915'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='academicyear',
            options={'ordering': ['year']},
        ),
        migrations.AlterField(
            model_name='course',
            name='number',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]
