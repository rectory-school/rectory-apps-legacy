# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('detention_notifier', '0012_auto_20160301_0815'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='detentioncc',
            unique_together=set([('mailer', 'address')]),
        ),
        migrations.AlterUniqueTogether(
            name='detentionerrornotification',
            unique_together=set([('mailer', 'address')]),
        ),
    ]
