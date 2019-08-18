# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courseevaluations', '0019_auto_20160108_1019'),
    ]

    operations = [
        migrations.CreateModel(
            name='MELPEvaluation',
            fields=[
                ('courseevaluation_ptr', models.OneToOneField(primary_key=True, parent_link=True, auto_created=True, to='courseevaluations.CourseEvaluation', serialize=False, on_delete=models.CASCADE)),
            ],
            options={
                'abstract': False,
            },
            bases=('courseevaluations.courseevaluation',),
        ),
    ]
