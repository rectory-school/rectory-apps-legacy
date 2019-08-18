# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import adminsortable.fields


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('academics', '0016_student_auth_key'),
    ]

    operations = [
        migrations.CreateModel(
            name='Evaluable',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EvaluationSet',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('available_until', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='FreeformQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('question', models.CharField(max_length=255)),
                ('question_order', models.PositiveIntegerField(editable=False, default=0, db_index=True)),
            ],
            options={
                'ordering': ['question_order'],
            },
        ),
        migrations.CreateModel(
            name='FreeformQuestionAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('answer', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='MultipleChoiceQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('question', models.CharField(max_length=255)),
                ('question_order', models.PositiveIntegerField(editable=False, default=0, db_index=True)),
            ],
            options={
                'ordering': ['question_order'],
            },
        ),
        migrations.CreateModel(
            name='MultipleChoiceQuestionAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='MultipleChoiceQuestionOption',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('option', models.CharField(max_length=255)),
                ('option_order', models.PositiveIntegerField(editable=False, default=0, db_index=True)),
                ('question', adminsortable.fields.SortableForeignKey(to='courseevaluations.MultipleChoiceQuestion', on_delete=models.CASCADE)),
            ],
            options={
                'ordering': ['option_order'],
            },
        ),
        migrations.CreateModel(
            name='QuestionSet',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='CourseEvaluation',
            fields=[
                ('evaluable_ptr', models.OneToOneField(to='courseevaluations.Evaluable', serialize=False, parent_link=True, auto_created=True, primary_key=True, on_delete=models.CASCADE)),
                ('section', models.ForeignKey(to='academics.Section', on_delete=models.CASCADE)),
            ],
            options={
                'abstract': False,
            },
            bases=('courseevaluations.evaluable',),
        ),
        migrations.CreateModel(
            name='DormEvaluation',
            fields=[
                ('evaluable_ptr', models.OneToOneField(to='courseevaluations.Evaluable', serialize=False, parent_link=True, auto_created=True, primary_key=True, on_delete=models.CASCADE)),
            ],
            options={
                'abstract': False,
            },
            bases=('courseevaluations.evaluable',),
        ),
        migrations.CreateModel(
            name='IIPEvaluation',
            fields=[
                ('evaluable_ptr', models.OneToOneField(to='courseevaluations.Evaluable', serialize=False, parent_link=True, auto_created=True, primary_key=True, on_delete=models.CASCADE)),
                ('teacher', models.ForeignKey(to='academics.Teacher', on_delete=models.CASCADE)),
            ],
            options={
                'abstract': False,
            },
            bases=('courseevaluations.evaluable',),
        ),
        migrations.AddField(
            model_name='multiplechoicequestionanswer',
            name='answer',
            field=models.ForeignKey(to='courseevaluations.MultipleChoiceQuestionOption', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='multiplechoicequestionanswer',
            name='evaluable',
            field=models.ForeignKey(to='courseevaluations.Evaluable', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='multiplechoicequestionanswer',
            name='student',
            field=models.ForeignKey(to='academics.Student', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='multiplechoicequestion',
            name='question_set',
            field=adminsortable.fields.SortableForeignKey(to='courseevaluations.QuestionSet', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='freeformquestionanswer',
            name='evaluable',
            field=models.ForeignKey(to='courseevaluations.Evaluable', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='freeformquestionanswer',
            name='question',
            field=models.ForeignKey(to='courseevaluations.FreeformQuestion', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='freeformquestion',
            name='question_set',
            field=adminsortable.fields.SortableForeignKey(to='courseevaluations.QuestionSet', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='evaluable',
            name='evaluation_set',
            field=models.ForeignKey(to='courseevaluations.EvaluationSet', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='evaluable',
            name='polymorphic_ctype',
            field=models.ForeignKey(related_name='polymorphic_courseevaluations.evaluable_set+', to='contenttypes.ContentType', null=True, editable=False, on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='evaluable',
            name='question_set',
            field=models.ForeignKey(to='courseevaluations.QuestionSet', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='evaluable',
            name='students',
            field=models.ManyToManyField(to='academics.Student'),
        ),
        migrations.CreateModel(
            name='DormParentEvaluation',
            fields=[
                ('dormevaluation_ptr', models.OneToOneField(to='courseevaluations.DormEvaluation', serialize=False, parent_link=True, auto_created=True, primary_key=True, on_delete=models.CASCADE)),
                ('parent', models.ForeignKey(to='academics.Teacher', on_delete=models.CASCADE)),
            ],
            options={
                'abstract': False,
            },
            bases=('courseevaluations.dormevaluation',),
        ),
        migrations.AddField(
            model_name='dormevaluation',
            name='dorm',
            field=models.ForeignKey(to='academics.Dorm', on_delete=models.CASCADE),
        ),
    ]
