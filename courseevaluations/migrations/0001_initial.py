# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import adminsortable.fields


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('academics', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseEvaluation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DormParentEvaluation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('dorm', models.ForeignKey(to='academics.Dorm')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EvaluationSet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=255)),
                ('available_until', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='FreeformQuestion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('question', models.CharField(max_length=255)),
                ('question_order', models.PositiveIntegerField(db_index=True, default=0, editable=False)),
            ],
            options={
                'ordering': ['question_order'],
            },
        ),
        migrations.CreateModel(
            name='IIPEvaluation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('evaluation_set', models.ForeignKey(to='courseevaluations.EvaluationSet')),
                ('polymorphic_ctype', models.ForeignKey(editable=False, related_name='polymorphic_courseevaluations.iipevaluation_set+', null=True, to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MultipleChoiceQuestion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('question', models.CharField(max_length=255)),
                ('question_order', models.PositiveIntegerField(db_index=True, default=0, editable=False)),
            ],
            options={
                'ordering': ['question_order'],
            },
        ),
        migrations.CreateModel(
            name='MultipleChoiceQuestionOption',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('option', models.CharField(max_length=255)),
                ('option_order', models.PositiveIntegerField(db_index=True, default=0, editable=False)),
                ('question', adminsortable.fields.SortableForeignKey(to='courseevaluations.MultipleChoiceQuestion')),
            ],
            options={
                'ordering': ['option_order'],
            },
        ),
        migrations.CreateModel(
            name='QuestionSet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='multiplechoicequestion',
            name='question_set',
            field=adminsortable.fields.SortableForeignKey(to='courseevaluations.QuestionSet'),
        ),
        migrations.AddField(
            model_name='iipevaluation',
            name='question_set',
            field=models.ForeignKey(to='courseevaluations.QuestionSet'),
        ),
        migrations.AddField(
            model_name='iipevaluation',
            name='students',
            field=models.ManyToManyField(to='academics.Student'),
        ),
        migrations.AddField(
            model_name='iipevaluation',
            name='teacher',
            field=models.ForeignKey(to='academics.Teacher'),
        ),
        migrations.AddField(
            model_name='freeformquestion',
            name='question_set',
            field=adminsortable.fields.SortableForeignKey(to='courseevaluations.QuestionSet'),
        ),
        migrations.AddField(
            model_name='dormparentevaluation',
            name='evaluation_set',
            field=models.ForeignKey(to='courseevaluations.EvaluationSet'),
        ),
        migrations.AddField(
            model_name='dormparentevaluation',
            name='parent',
            field=models.ForeignKey(to='academics.Teacher'),
        ),
        migrations.AddField(
            model_name='dormparentevaluation',
            name='polymorphic_ctype',
            field=models.ForeignKey(editable=False, related_name='polymorphic_courseevaluations.dormparentevaluation_set+', null=True, to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='dormparentevaluation',
            name='question_set',
            field=models.ForeignKey(to='courseevaluations.QuestionSet'),
        ),
        migrations.AddField(
            model_name='dormparentevaluation',
            name='students',
            field=models.ManyToManyField(to='academics.Student'),
        ),
        migrations.AddField(
            model_name='courseevaluation',
            name='evaluation_set',
            field=models.ForeignKey(to='courseevaluations.EvaluationSet'),
        ),
        migrations.AddField(
            model_name='courseevaluation',
            name='polymorphic_ctype',
            field=models.ForeignKey(editable=False, related_name='polymorphic_courseevaluations.courseevaluation_set+', null=True, to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='courseevaluation',
            name='question_set',
            field=models.ForeignKey(to='courseevaluations.QuestionSet'),
        ),
        migrations.AddField(
            model_name='courseevaluation',
            name='section',
            field=models.ForeignKey(to='academics.Section'),
        ),
        migrations.AddField(
            model_name='courseevaluation',
            name='students',
            field=models.ManyToManyField(to='academics.Student'),
        ),
    ]
