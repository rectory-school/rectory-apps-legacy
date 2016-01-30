# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calendar_generator', '0002_auto_20160129_1455'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='skipdate',
            options={'ordering': ['date']},
        ),
    ]
