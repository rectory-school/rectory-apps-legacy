# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courseevaluations', '0008_freeformquestionanswer_question'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='evaluationset',
            options={'permissions': (('can_view_status_reports', 'Can view status reports'), ('can_view_student_links', 'Can view student links'))},
        ),
    ]
