# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seating_charts', '0006_auto_20160203_1332'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mealtime',
            options={'ordering': ['order']},
        ),
        migrations.AddField(
            model_name='historicalmealtime',
            name='order',
            field=models.PositiveIntegerField(default=0, editable=False, db_index=True),
        ),
        migrations.AddField(
            model_name='mealtime',
            name='order',
            field=models.PositiveIntegerField(default=0, editable=False, db_index=True),
        ),
    ]
