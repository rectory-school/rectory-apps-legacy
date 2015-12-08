# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courseevaluations', '0003_auto_20151208_0954'),
    ]

    operations = [
        migrations.AddField(
            model_name='freeformquestion',
            name='required',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='multiplechoicequestion',
            name='required',
            field=models.BooleanField(default=True),
        ),
    ]
