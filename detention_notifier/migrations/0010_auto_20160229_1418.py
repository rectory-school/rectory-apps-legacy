# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('detention_notifier', '0009_auto_20160229_1413'),
    ]

    operations = [
        migrations.AddField(
            model_name='detentionmailer',
            name='advisor_mail',
            field=models.CharField(max_length=3, choices=[('', 'None'), ('to', 'To'), ('cc', 'Cc'), ('bcc', 'Bcc')], default=''),
        ),
        migrations.AddField(
            model_name='detentionmailer',
            name='reply_to_advisor',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='detentionmailer',
            name='reply_to_tutor',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='detentionmailer',
            name='tutor_mail',
            field=models.CharField(max_length=3, choices=[('', 'None'), ('to', 'To'), ('cc', 'Cc'), ('bcc', 'Bcc')], default=''),
        ),
    ]
