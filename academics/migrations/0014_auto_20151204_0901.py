# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0013_auto_20151204_0858'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentRegistration',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('student_reg_id', models.CharField(unique=True, max_length=20)),
                ('section', models.ForeignKey(to='academics.Section', on_delete=models.CASCADE)),
                ('student', models.ForeignKey(to='academics.Student', on_delete=models.CASCADE)),
            ],
        ),
        migrations.AddField(
            model_name='section',
            name='students',
            field=models.ManyToManyField(through='academics.StudentRegistration', to='academics.Student'),
        ),
    ]
