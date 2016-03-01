# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('detention_notifier', '0013_auto_20160301_1031'),
    ]

    operations = [
        migrations.CreateModel(
            name='DetentionTo',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('family_id_key', models.CharField(max_length=9, choices=[('IDFamily1', 'Family 1'), ('IDFamily2', 'Family 2'), ('IDFamily3', 'Family 3'), ('IDFamily4', 'Family 4')], verbose_name='Family')),
                ('parent_code', models.CharField(max_length=9, choices=[('a', 'Parent A'), ('b', 'Parent B')], verbose_name='Parent Code')),
                ('mailer', models.ForeignKey(to='detention_notifier.DetentionMailer')),
            ],
        ),
    ]
