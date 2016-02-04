# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0029_historicalparent_historicalstudentparentrelation'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='parents',
            field=models.ManyToManyField(to='academics.Parent', blank=True, through='academics.StudentParentRelation'),
        ),
    ]
