# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('enrichmentmanager', '0026_emailsuppression'),
    ]

    operations = [
        migrations.RenameField(
            model_name='emailsuppression',
            old_name='date',
            new_name='suppression_date',
        ),
    ]
