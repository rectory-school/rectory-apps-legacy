# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0016_student_auth_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='rectory_password',
            field=models.CharField(max_length=254, blank=True),
        ),
    ]
