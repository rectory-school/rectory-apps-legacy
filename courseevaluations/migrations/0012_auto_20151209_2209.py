# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courseevaluations', '0011_auto_20151209_1452'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='evaluationset',
            options={'permissions': (('can_view_status_reports', 'Can view status reports'), ('can_view_student_links', 'Can view student links'), ('can_send_emails', 'Can send e-mails'))},
        ),
        migrations.AddField(
            model_name='studentemailtemplate',
            name='content_subtype',
            field=models.CharField(default='plain', max_length=5, choices=[('html', 'HTML'), ('plain', 'Plain Text')]),
        ),
    ]
