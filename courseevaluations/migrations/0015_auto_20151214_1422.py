# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courseevaluations', '0014_auto_20151211_1017'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='evaluationset',
            options={'ordering': ['created_at'], 'permissions': (('can_view_status_reports', 'Can view status reports'), ('can_view_results', 'Can view results'), ('can_view_student_links', 'Can view student links'), ('can_send_emails', 'Can send e-mails'), ('can_create_evaluables', 'Can create evaluables'))},
        ),
    ]
