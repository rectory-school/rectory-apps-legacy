# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import adminsortable.fields


class Migration(migrations.Migration):

    dependencies = [
        ('courseevaluations', '0002_multiplechoicequestion_question_set'),
    ]

    operations = [
        migrations.CreateModel(
            name='FreeFormQuestion',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('question', models.CharField(max_length=255)),
                ('question_order', models.PositiveIntegerField(db_index=True, editable=False, default=0)),
                ('question_set', adminsortable.fields.SortableForeignKey(to='courseevaluations.QuestionSet')),
            ],
            options={
                'ordering': ['question_order'],
            },
        ),
    ]
