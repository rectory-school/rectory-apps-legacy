# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0035_auto_20160209_1329'),
    ]

    operations = [
        migrations.CreateModel(
            name='Term',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('term', models.CharField(max_length=255)),
                ('academic_year', models.ForeignKey(to='academics.AcademicYear', on_delete=models.CASCADE)),
            ],
        ),
    ]
