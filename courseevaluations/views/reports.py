#!/usr/bin/python

from datetime import date

from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.db.models import Count, Case, When
from django.http import HttpResponse

from academics.models import Student, Section
from courseevaluations.models import EvaluationSet, Evaluable, CourseEvaluation, IIPEvaluation, DormParentEvaluation, StudentEmailTemplate
from courseevaluations.lib.async import send_student_email_from_template, send_confirmation_email

from django.contrib.auth.decorators import permission_required

import django_rq

import courseevaluations.lib.reporting

@permission_required('courseevaluations.can_view_status_reports')
def index(request, id):
    evaluation_set = get_object_or_404(EvaluationSet, pk=id)
    
    evaluables = Evaluable.objects.filter(evaluation_set=evaluation_set)
    
    complete_evaluables = evaluables.filter(complete=True)
    incomplete_evaluables = evaluables.filter(complete=False)
    
    template_vars = {
        'evaluables': evaluables,
        'evaluables_complete': complete_evaluables, 
        'evaluables_incomplete': incomplete_evaluables,
        'evaluation_set': evaluation_set,
        'percent_completed': (complete_evaluables.count() / evaluables.count() * 100),
        'student_email_templates': StudentEmailTemplate.objects.all()
    }
    
    return render(request, "courseevaluations/reports/index.html", template_vars)

@permission_required('courseevaluations.can_view_status_reports')
def by_student(request, id, show_evaluables):
    evaluation_set = get_object_or_404(EvaluationSet, pk=id)

    show_links = (request.GET.get('show_links', "false").lower() == "true")
    
    if show_links:
        if not request.user or not request.user.has_perm("courseevaluations.can_view_student_links"):
            show_links = False

    students = Student.objects.filter(evaluable__evaluation_set=evaluation_set)
    
    students = students.annotate(complete_count=Count(Case(When(
        evaluable__complete=True,
        evaluable__evaluation_set=evaluation_set,
        then=1
        ))))
        
    students = students.annotate(incomplete_count=Count(Case(When(
        evaluable__complete=False,
        evaluable__evaluation_set=evaluation_set,
        then=1
        ))))
    
    students = students.annotate(total_count=Count(Case(When(
        evaluable__evaluation_set=evaluation_set,
        then=1
        ))))
        
    complete = []
    incomplete = []
    
    for s in students:
        if s.incomplete_count == 0:
            complete.append(s)
        else:
            incomplete.append(s)
    
    template_vars = {
        'evaluation_set': evaluation_set,
        'complete': complete,
        'incomplete': incomplete,
        'show_evaluables': show_evaluables,
        'show_links': show_links,
    }
    
    return render(request, "courseevaluations/reports/by_student.html", template_vars)

@permission_required('courseevaluations.can_view_status_reports')
def by_section(request, id):
    evaluation_set = get_object_or_404(EvaluationSet, pk=id)
    
    data = courseevaluations.lib.reporting.get_incomplete_evaluables_by_teacher(evaluation_set)
    
    flattened_data = courseevaluations.lib.reporting.flatten_evaluables_by_teacher(data)
    
    template_vars = {'report_data': flattened_data, 'evaluation_set': evaluation_set}
        
    return render(request, "courseevaluations/reports/by_section.html", template_vars)

@permission_required('courseevaluations.can_send_emails')
def send_student_email(request):
    template_id = request.POST["student_email_template"]
    operation = request.POST["send_type"]
    
    template = StudentEmailTemplate.objects.get(pk=template_id)
    
    evaluation_sets = EvaluationSet.objects.open()
    
    to_students = []
    confirmation_addresses = []
    
    if operation == "sample":
        evaluable = Evaluable.objects.filter(evaluation_set__in=evaluation_sets).order_by("?").first()
        student = evaluable.student
        
        django_rq.enqueue(send_student_email_from_template, template.id, student.id, override_email=request.user.email)
        
        return HttpResponse("Your sample is on the way", content_type="text/plain")
        
    elif operation == "redirect":
        evaluables = Evaluable.objects.filter(evaluation_set__in=evaluation_sets)
        students = Student.objects.filter(evaluable__in=evaluables).distinct()
        
        for student in students:
            to_students.append(student)
            django_rq.enqueue(send_student_email_from_template, template.id, student.id, override_email=request.user.email)
            
        return HttpResponse("All {count:} student e-mails have been generated and are being redirected to you.".format(count=len(to_students)), content_type="text/plain")
            
    elif operation == "send":
        evaluables = Evaluable.objects.filter(evaluation_set__in=evaluation_sets)
        students = Student.objects.filter(evaluable__in=evaluables).distinct()
        
        confirmation_addresses = []
        
        for student in students:
            to_students.append(student)
            django_rq.enqueue(send_student_email_from_template, template.id, student.id)
            confirmation_addresses.append(student.email)
        
        django_rq.enqueue(send_confirmation_email, confirmation_addresses, [request.user.email])
        
        return HttpResponse("All {count:} student e-mails have been generated and are on their way.".format(count=len(to_students)), content_type="text/plain")
