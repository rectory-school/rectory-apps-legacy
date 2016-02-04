# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0027_auto_20160204_1133'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='parent',
            options={'ordering': ['last_name', 'first_name']},
        ),
    ]
