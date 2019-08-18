# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('detention_notifier', '0002_offense_mail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detention',
            name='student',
            field=models.ForeignKey(null=True, to='academics.Student', on_delete=models.CASCADE),
        ),
        migrations.AlterField(
            model_name='detention',
            name='teacher',
            field=models.ForeignKey(null=True, to='academics.Teacher', on_delete=models.CASCADE),
        ),
        migrations.AlterField(
            model_name='detention',
            name='term',
            field=models.ForeignKey(null=True, to='academics.Term', on_delete=models.CASCADE),
        ),
    ]
