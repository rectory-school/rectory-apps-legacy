# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('detention_notifier', '0007_detention_sent'),
    ]

    operations = [
        migrations.CreateModel(
            name='DetentionCC',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('address', models.EmailField(max_length=254)),
                ('mail_type', models.CharField(choices=[('to', 'To'), ('cc', 'Cc'), ('bcc', 'Bcc')], max_length=3)),
            ],
        ),
        migrations.AddField(
            model_name='detentionmailer',
            name='blank_code',
            field=models.ForeignKey(to='detention_notifier.Code', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='detentioncc',
            name='mailer',
            field=models.ForeignKey(to='detention_notifier.DetentionMailer'),
        ),
    ]
