# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courseevaluations', '0005_auto_20151208_1014'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='iipevaluation',
            options={'verbose_name': 'IIP evaluation'},
        ),
    ]
