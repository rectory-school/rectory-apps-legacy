# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0021_grade_normalization'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='grade',
            options={'ordering': ['grade']},
        ),
    ]
