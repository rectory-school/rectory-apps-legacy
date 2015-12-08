# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courseevaluations', '0002_auto_20151208_0952'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionset',
            name='name',
            field=models.CharField(unique=True, max_length=255),
        ),
    ]
