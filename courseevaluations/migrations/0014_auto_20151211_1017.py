# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courseevaluations', '0013_evaluationset_created_at'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='evaluationset',
            options={'ordering': ['created_at'], 'permissions': (('can_view_status_reports', 'Can view status reports'), ('can_view_student_links', 'Can view student links'), ('can_send_emails', 'Can send e-mails'))},
        ),
    ]
