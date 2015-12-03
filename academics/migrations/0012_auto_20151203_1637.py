# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0011_auto_20151203_1617'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='enrollment',
            options={'ordering': ['student__last_name', 'student__first_name', 'academic_year__year']},
        ),
        migrations.AlterModelOptions(
            name='student',
            options={'ordering': ('last_name', 'first_name')},
        ),
    ]
