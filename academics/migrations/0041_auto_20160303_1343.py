# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0040_auto_20160301_1031'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='parent',
            options={'ordering': ['last_name', 'first_name'], 'permissions': (('can_download_family_data', 'Can download family data'),)},
        ),
    ]
