# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0016_student_auth_key'),
        ('courseevaluations', '0004_auto_20151208_1004'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='evaluable',
            name='students',
        ),
        migrations.RemoveField(
            model_name='freeformquestionanswer',
            name='question',
        ),
        migrations.RemoveField(
            model_name='multiplechoicequestionanswer',
            name='student',
        ),
        migrations.AddField(
            model_name='evaluable',
            name='student',
            field=models.ForeignKey(to='academics.Student', default=None),
            preserve_default=False,
        ),
    ]
