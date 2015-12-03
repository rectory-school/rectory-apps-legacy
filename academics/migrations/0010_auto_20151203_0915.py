# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0009_auto_20151203_0908'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dorm',
            options={'ordering': ['building', 'wing', 'level']},
        ),
        migrations.AlterField(
            model_name='dorm',
            name='heads',
            field=models.ManyToManyField(blank=True, to='academics.Teacher', verbose_name='dorm parents', related_name='_heads_+'),
        ),
    ]
