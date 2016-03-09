# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courseevaluations', '0020_melpevaluation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='melpevaluation',
            name='courseevaluation_ptr',
        ),
        migrations.DeleteModel(
            name='MELPEvaluation',
        ),
    ]
