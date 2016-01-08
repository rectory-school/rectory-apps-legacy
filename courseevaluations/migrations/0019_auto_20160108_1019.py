# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courseevaluations', '0018_auto_20160108_1012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evaluable',
            name='enrollment',
            field=models.ForeignKey(to='academics.Enrollment'),
        ),
    ]
