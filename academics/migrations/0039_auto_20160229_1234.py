# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0038_auto_20160229_1120'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='term',
            options={'ordering': ['academic_year__year', 'term']},
        ),
    ]
