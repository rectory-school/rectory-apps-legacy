# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paw', '0011_entrypoint'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entrypoint',
            name='domain',
            field=models.CharField(unique=True, blank=True, max_length=254),
        ),
    ]
