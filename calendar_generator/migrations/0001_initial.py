# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import adminsortable.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Calendar',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('title', models.CharField(max_length=254)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('sunday', models.BooleanField(default=False)),
                ('monday', models.BooleanField(default=True)),
                ('tuesday', models.BooleanField(default=True)),
                ('wednesday', models.BooleanField(default=True)),
                ('thursday', models.BooleanField(default=True)),
                ('friday', models.BooleanField(default=True)),
                ('saturday', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Day',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('letter', models.CharField(max_length=1)),
                ('day_order', models.PositiveIntegerField(editable=False, default=0, db_index=True)),
                ('calendar', adminsortable.fields.SortableForeignKey(to='calendar_generator.Calendar', on_delete=models.CASCADE)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ResetDate',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('date', models.DateField()),
                ('calendar', models.ForeignKey(to='calendar_generator.Calendar', on_delete=models.CASCADE)),
                ('day', models.ForeignKey(to='calendar_generator.Day', on_delete=models.CASCADE)),
            ],
        ),
        migrations.CreateModel(
            name='SkipDate',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('date', models.DateField()),
                ('calendar', models.ForeignKey(to='calendar_generator.Calendar', on_delete=models.CASCADE)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='skipdate',
            unique_together=set([('calendar', 'date')]),
        ),
    ]
