#!/usr/bin/python

from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import permission_required

from academics.models import Course, Section, Teacher, Dorm
from courseevaluations.models import CourseEvaluation, DormParentEvaluation, IIPEvaluation, EvaluationSet

from courseevaluations.lib.results import build_report

@permission_required('courseevaluations.can_view_results')
def teacher(request, evaluation_set_id, teacher_id):
    teacher = Teacher.objects.get(pk=teacher_id)
    evaluation_set = EvaluationSet.objects.get(pk=evaluation_set_id)
    
    evaluables = CourseEvaluation.objects.filter(section__teacher=teacher, evaluation_set=evaluation_set)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report.pdf"'
    
    title = "All evaluations for {teacher:} ({evaluation_set:})".format(
        teacher=teacher.name,
        evaluation_set=evaluation_set.name
        )
    
    build_report(response, evaluables, title=title)
    
    return response

@permission_required('courseevaluations.can_view_results')
def teacher_course(request, evaluation_set_id, teacher_id, course_id):
    course = Course.objects.get(pk=course_id)
    teacher = Teacher.objects.get(pk=teacher_id)
    evaluation_set = EvaluationSet.objects.get(pk=evaluation_set_id)
    
    sections = Section.objects.filter(course=course)
    
    evaluables = CourseEvaluation.objects.filter(section__in=sections, evaluation_set=evaluation_set)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report.pdf"'
    
    title = "{course:} with {teacher:} ({evaluation_set:})".format(
        course=course.course_name,
        teacher=teacher.name,
        evaluation_set=evaluation_set.name
        )
    
    build_report(response, evaluables, title=title)
    
    return response

@permission_required('courseevaluations.can_view_results')
def section(request, evaluation_set_id, section_id):
    section = Section.objects.get(pk=section_id)
    evaluation_set = EvaluationSet.objects.get(pk=evaluation_set_id)
    
    evaluables = CourseEvaluation.objects.filter(section=section, evaluation_set=evaluation_set)
    
    response = HttpResponse(content_type='application/pdf')
    
    title = "{course:}: {section:} with {teacher:} ({evaluation_set:})".format(
        course = section.course.course_name,
        section=section.csn,
        teacher=section.teacher.name,
        evaluation_set=evaluation_set.name
        )
    
    build_report(response, evaluables, title=title)
    
    return response

@permission_required('courseevaluations.can_view_results')
def iip(request, evaluation_set_id, teacher_id):
    evaluation_set = EvaluationSet.objects.get(pk=evaluation_set_id)
    teacher = Teacher.objects.get(pk=teacher_id)
    
    evaluables = IIPEvaluation.objects.filter(evaluation_set=evaluation_set, teacher=teacher)
    
    response = HttpResponse(content_type='application/pdf')
    
    title = "IIP with {teacher:} ({evaluation_set:})".format(
        teacher=teacher.name,
        evaluation_set=evaluation_set.name
        )
    
    build_report(response, evaluables, title=title)
    
    return response

@permission_required('courseevaluations.can_view_results')
def dorm_parent_dorm_parent(request, evaluation_set_id, dorm_id, parent_id):
    evaluation_set = EvaluationSet.objects.get(pk=evaluation_set_id)
    dorm = Dorm.objects.get(pk=dorm_id)
    parent = Teacher.objects.get(pk=parent_id)
    
    evaluables = DormParentEvaluation.objects.filter(evaluation_set=evaluation_set, dorm=dorm, parent=parent)
    
    response = HttpResponse(content_type='application/pdf')
    
    title = "{dorm:} with {parent:} ({evaluation_set:})".format(
        dorm = str(dorm),
        parent=parent.name,
        evaluation_set=evaluation_set.name
        )
    
    build_report(response, evaluables, title=title)
    
    return response

@permission_required('courseevaluations.can_view_results')
def dorm_parent_dorm(request, evaluation_set_id, dorm_id):
    evaluation_set = EvaluationSet.objects.get(pk=evaluation_set_id)
    dorm = Dorm.objects.get(pk=dorm_id)
    
    evaluables = DormParentEvaluation.objects.filter(evaluation_set=evaluation_set, dorm=dorm)
    
    response = HttpResponse(content_type='application/pdf')
    
    title = "Dorm Parent Evaluation for {dorm:} ({evaluation_set:})".format(
        dorm = str(dorm),
        evaluation_set=evaluation_set.name
        )
    
    build_report(response, evaluables, title=title)
    
    return response

@permission_required('courseevaluations.can_view_results')
def dorm_parent_parent(request, evaluation_set_id, parent_id):
    evaluation_set = EvaluationSet.objects.get(pk=evaluation_set_id)
    parent = Teacher.objects.get(pk=parent_id)
    
    evaluables = DormParentEvaluation.objects.filter(evaluation_set=evaluation_set, parent=parent)
    
    response = HttpResponse(content_type='application/pdf')
    
    title = "Dorm Parent Evaluation for {parent:} ({evaluation_set:})".format(
        parent=parent.name,
        evaluation_set=evaluation_set.name
        )
    
    build_report(response, evaluables, title=title)
    
    return response

@permission_required('courseevaluations.can_view_results')
def index(request, evaluation_set_id):
    evaluation_set = EvaluationSet.objects.get(pk=evaluation_set_id)
    
    course_evaluables = CourseEvaluation.objects.filter(evaluation_set=evaluation_set)
    dorm_parent_evaluables = DormParentEvaluation.objects.filter(evaluation_set=evaluation_set)
    iip_evaluables = IIPEvaluation.objects.filter(evaluation_set=evaluation_set)
    
    sections = Section.objects.filter(courseevaluation__in=course_evaluables).distinct()
    iip_teachers = Teacher.objects.filter(iipevaluation__in=iip_evaluables).order_by('last_name', 'first_name').distinct()
    
    dorm_parents = []
    for evaluable in dorm_parent_evaluables:
        d = {'dorm': evaluable.dorm, 'parent': evaluable.parent}
        if not d in dorm_parents:
            dorm_parents.append(d)
    
    return render(request, "courseevaluations/results/index.html", {'evaluation_set': evaluation_set, 'sections': sections, 'iip_teachers': iip_teachers, 'dorm_parents': dorm_parents})