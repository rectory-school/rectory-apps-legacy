# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0012_auto_20151203_1637'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='section',
            unique_together=set([('csn', 'academic_year')]),
        ),
    ]
