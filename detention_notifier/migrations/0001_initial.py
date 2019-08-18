# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0036_term'),
    ]

    operations = [
        migrations.CreateModel(
            name='Detention',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('incident_id', models.PositiveIntegerField(unique=True)),
                ('detention_date', models.DateField()),
                ('code', models.CharField(max_length=254)),
                ('comments', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='DetentionMailer',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('from_name', models.CharField(max_length=255)),
                ('from_email', models.EmailField(max_length=255)),
                ('detention_protol', models.TextField()),
                ('signature', models.TextField()),
                ('skip_processing_before', models.DateField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Offense',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('offense', models.CharField(unique=True, max_length=255)),
                ('sentence_insert', models.CharField(max_length=4096)),
            ],
        ),
        migrations.AddField(
            model_name='detention',
            name='offense',
            field=models.ForeignKey(to='detention_notifier.Offense', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='detention',
            name='student',
            field=models.ForeignKey(to='academics.Student', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='detention',
            name='teacher',
            field=models.ForeignKey(to='academics.Teacher', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='detention',
            name='term',
            field=models.ForeignKey(to='academics.Term', on_delete=models.CASCADE),
        ),
    ]
