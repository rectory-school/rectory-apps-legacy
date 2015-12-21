# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0017_student_rectory_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='username',
            field=models.CharField(blank=True, max_length=254),
        ),
    ]
