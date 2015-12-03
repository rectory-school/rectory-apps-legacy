# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0008_auto_20151203_0906'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='teacher',
            options={'ordering': ['last_name', 'first_name']},
        ),
        migrations.AlterField(
            model_name='dorm',
            name='heads',
            field=models.ManyToManyField(blank=True, related_name='_heads_+', to='academics.Teacher'),
        ),
    ]
