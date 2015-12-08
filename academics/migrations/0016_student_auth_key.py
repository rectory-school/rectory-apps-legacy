# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import academics.models


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0015_auto_20151204_1107'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='auth_key',
            field=models.CharField(default=academics.models.default_auth_key, max_length=63),
        ),
    ]
