# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import adminsortable.fields


class Migration(migrations.Migration):

    dependencies = [
        ('courseevaluations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='multiplechoicequestion',
            name='question_set',
            field=adminsortable.fields.SortableForeignKey(to='courseevaluations.QuestionSet', default=0),
            preserve_default=False,
        ),
    ]
