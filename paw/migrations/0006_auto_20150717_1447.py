# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('paw', '0005_pageicon_start_hidden'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pageicon',
            options={'ordering': ['title']},
        ),
    ]
