# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0043_auto_20160309_0958'),
        ('courseevaluations', '0021_auto_20160309_1128'),
    ]

    operations = [
        migrations.CreateModel(
            name='MELPEvaluation',
            fields=[
                ('evaluable_ptr', models.OneToOneField(parent_link=True, primary_key=True, to='courseevaluations.Evaluable', auto_created=True, serialize=False, on_delete=models.CASCADE)),
                ('section', models.ForeignKey(to='academics.Section', on_delete=models.CASCADE)),
            ],
            options={
                'abstract': False,
            },
            bases=('courseevaluations.evaluable',),
        ),
    ]
