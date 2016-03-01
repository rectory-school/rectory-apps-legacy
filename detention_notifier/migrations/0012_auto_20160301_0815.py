# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('detention_notifier', '0011_detentionmailer_reply_to_from'),
    ]

    operations = [
        migrations.CreateModel(
            name='DetentionErrorNotification',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('address', models.EmailField(max_length=254)),
            ],
            options={
                'verbose_name': 'Error recipient',
            },
        ),
        migrations.AlterModelOptions(
            name='detentioncc',
            options={'verbose_name_plural': 'Additional addresses', 'verbose_name': 'Additional address'},
        ),
        migrations.AlterField(
            model_name='detentionmailer',
            name='advisor_mail',
            field=models.CharField(blank=True, choices=[('', 'None'), ('to', 'To'), ('cc', 'Cc'), ('bcc', 'Bcc')], max_length=3, verbose_name='Advisor e-mail'),
        ),
        migrations.AlterField(
            model_name='detentionmailer',
            name='reply_to_advisor',
            field=models.BooleanField(default=True, verbose_name='Reply-to advisor'),
        ),
        migrations.AlterField(
            model_name='detentionmailer',
            name='reply_to_from',
            field=models.BooleanField(default=True, verbose_name='Reply-to address above'),
        ),
        migrations.AlterField(
            model_name='detentionmailer',
            name='reply_to_tutor',
            field=models.BooleanField(default=False, verbose_name='Reply-to tutor'),
        ),
        migrations.AlterField(
            model_name='detentionmailer',
            name='tutor_mail',
            field=models.CharField(blank=True, choices=[('', 'None'), ('to', 'To'), ('cc', 'Cc'), ('bcc', 'Bcc')], max_length=3, verbose_name='Tutor e-mail'),
        ),
        migrations.AddField(
            model_name='detentionerrornotification',
            name='mailer',
            field=models.ForeignKey(to='detention_notifier.DetentionMailer'),
        ),
    ]
