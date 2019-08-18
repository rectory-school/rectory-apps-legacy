# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('detention_notifier', '0008_auto_20160229_1407'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='detentioncc',
            options={'verbose_name': 'Detention CC'},
        ),
        migrations.RemoveField(
            model_name='detentionmailer',
            name='blank_code',
        ),
        migrations.AddField(
            model_name='detentionmailer',
            name='blank_offense',
            field=models.ForeignKey(blank=True, to='detention_notifier.Offense', null=True, on_delete=models.CASCADE),
        ),
    ]
