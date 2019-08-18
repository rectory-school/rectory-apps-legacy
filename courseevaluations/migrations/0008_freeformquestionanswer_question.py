# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courseevaluations', '0007_evaluable_complete'),
    ]

    operations = [
        migrations.AddField(
            model_name='freeformquestionanswer',
            name='question',
            field=models.ForeignKey(default=0, to='courseevaluations.FreeformQuestion', on_delete=models.CASCADE),
            preserve_default=False,
        ),
    ]
