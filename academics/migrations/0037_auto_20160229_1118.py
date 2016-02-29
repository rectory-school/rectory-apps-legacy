# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0036_term'),
    ]

    operations = [
        migrations.AlterField(
            model_name='term',
            name='term',
            field=models.CharField(max_length=2),
        ),
    ]
