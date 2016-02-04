# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0023_auto_20160203_1332'),
    ]

    operations = [
        migrations.AddField(
            model_name='grade',
            name='school',
            field=models.CharField(max_length=10, blank=True, choices=[('', '--'), ('elementary', 'Elementary School'), ('middle', 'Middle School'), ('high', 'High School')], default=''),
        ),
    ]
