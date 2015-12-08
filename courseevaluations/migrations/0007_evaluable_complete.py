# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courseevaluations', '0006_auto_20151208_1046'),
    ]

    operations = [
        migrations.AddField(
            model_name='evaluable',
            name='complete',
            field=models.BooleanField(default=False),
        ),
    ]
