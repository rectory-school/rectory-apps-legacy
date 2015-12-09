# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courseevaluations', '0010_studentemailtemplate'),
    ]

    operations = [
        migrations.RenameField(
            model_name='studentemailtemplate',
            old_name='template',
            new_name='body',
        ),
    ]
