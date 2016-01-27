# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paw', '0008_auto_20160127_1327'),
    ]

    operations = [
        migrations.RenameField(
            model_name='textlink',
            old_name='url',
            new_name='explicit_url',
        ),
    ]
