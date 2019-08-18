# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0025_parent'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentParentRelation',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('relationship', models.CharField(blank=True, max_length=20)),
            ],
        ),
        migrations.AlterField(
            model_name='parent',
            name='phone_cell',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='parent',
            name='phone_home',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='parent',
            name='phone_work',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='studentparentrelation',
            name='parent',
            field=models.ForeignKey(to='academics.Parent', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='studentparentrelation',
            name='student',
            field=models.ForeignKey(to='academics.Student', on_delete=models.CASCADE),
        ),
        migrations.AlterUniqueTogether(
            name='studentparentrelation',
            unique_together=set([('student', 'parent')]),
        ),
    ]
