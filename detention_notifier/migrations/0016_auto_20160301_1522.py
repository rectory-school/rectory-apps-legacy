# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('detention_notifier', '0015_auto_20160301_1232'),
    ]

    operations = [
        migrations.RenameField(
            model_name='detentionmailer',
            old_name='detention_protol',
            new_name='middle_section',
        ),
        migrations.AddField(
            model_name='detentionmailer',
            name='assigner_mail',
            field=models.CharField(choices=[('', 'None'), ('to', 'To'), ('cc', 'Cc'), ('bcc', 'Bcc')], max_length=3, verbose_name='Assigner e-mail', blank=True),
        ),
        migrations.AddField(
            model_name='detentionmailer',
            name='reply_to_assigner',
            field=models.BooleanField(default=False, verbose_name='Reply-to detention assigner'),
        ),
    ]
