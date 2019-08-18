#!/usr/bin/python

from datetime import date
from random import choice
from io import StringIO

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.db.models import Count, Case, When
from django.http import HttpResponse
from django.conf import settings
from django.core.mail import EmailMessage

from academics.models import Student, Section, Course, AcademicYear, Enrollment, StudentRegistration
from courseevaluations.models import EvaluationSet, Evaluable, CourseEvaluation, IIPEvaluation, DormParentEvaluation, StudentEmailTemplate
from courseevaluations.lib.async_funcs import send_student_email_from_template, send_confirmation_email, send_msg
from courseevaluations.lib.reporting import get_incomplete_evaluables_by_teacher

from django.contrib.auth.decorators import permission_required

import django_rq

import courseevaluations.lib.reporting 

@permission_required('courseevaluations.can_view_status_reports')
def index(request):
    evaluation_sets = EvaluationSet.objects.all()
    
    flattened_evaluation_sets = []
    
    for evaluation_set in evaluation_sets:
        flattened_evaluation_sets.append({
            'evaluation_set': evaluation_set, 
            'complete_count': evaluation_set.evaluable_set.filter(complete=True).count(), 
            'incomplete_count': evaluation_set.evaluable_set.filter(complete=False).count(), 
            'total_count': evaluation_set.evaluable_set.count(), 
        })
    
    return render(request, "courseevaluations/reports/index.html", {'evaluation_sets': flattened_evaluation_sets})

@permission_required('courseevaluations.can_view_status_reports')
def evaluation_set_index(request, id):
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
    
    return render(request, "courseevaluations/reports/evaluation_set_index.html", template_vars)

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
    
    #Do the grouping here to save round trips to the database
    if show_evaluables:
        all_evaluables = Evaluable.objects.filter(student__in=students, evaluation_set=evaluation_set).prefetch_related('student')
    
        grouped_evaluables = {}
        
        for evaluable in all_evaluables:
            if not evaluable.student in grouped_evaluables:
                grouped_evaluables[evaluable.student] = []
            
            grouped_evaluables[evaluable.student].append(evaluable)
            
    complete = []
    incomplete = []
    
    for student in students:
        #Where we're ultimately going to be dumping the student
        if student.incomplete_count == 0:
            output_list = complete
        else:
            output_list = incomplete
        
        if show_evaluables:
            output_list.append((student, grouped_evaluables[student]))
        else:
            output_list.append((student, []))
                
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
    
    if not evaluation_sets:
        return HttpResponse("Error: There are no open evaluation sets to send an e-mail for.")
    
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

@permission_required('courseevaluations.can_send_emails')
def send_teacher_per_section_email(request):
    evaluation_set_id = request.POST["evaluation_set_id"]
    operation = request.POST['send_type']
    
    evaluation_set = EvaluationSet.objects.get(pk=evaluation_set_id)
    
    if not evaluation_set.is_open:
        return HttpResponse("Error: This evaluation set is closed")
    
    data = get_incomplete_evaluables_by_teacher(evaluation_set)
    confirmation_addresses = []
    
    def generate_message(teacher):
        body = StringIO()
        
        body.write("Incomplete evaluations for {}\n\n".format(teacher.name))
        
        msg = EmailMessage()
        msg.to = [teacher.email]
        
        if 'course' in data[teacher]:
            for section in sorted(data[teacher]['course'].keys(), key=lambda sec: (sec.course.course_name, sec.csn)):
                body.write("{course:}: {csn:}\n".format(course=section.course.course_name, csn=section.csn))
                
                for student in sorted(data[teacher]['course'][section], key=lambda stu: (stu.last_name, stu.first_name)):
                    body.write("\t {first:} {last:}\n".format(first=student.first_name, last=student.last_name))
                
                body.write("\n")
        
        if 'iip' in data[teacher]:
            body.write("IIP\n")
            
            for student in sorted(data[teacher]['iip'], key=lambda stu: (stu.last_name, stu.first_name)):
                body.write("\t {first:} {last:}\n".format(first=student.first_name, last=student.last_name))
            
            body.write("\n")
        
        if 'dorm' in data[teacher]:
            for dorm in sorted(data[teacher]['dorm'].keys(), key=lambda d: (str(d))):
                body.write(str(dorm) + "\n")
                
                for student in sorted(data[teacher]['dorm'][dorm], key=lambda stu: (stu.last_name, stu.first_name)):
                    body.write("\t {first:} {last:}\n".format(first=student.first_name, last=student.last_name))
                
                body.write("\n")
        
        msg.subject = "Students that have not completed their evaluations for you"
        msg.body = body.getvalue()
        msg.from_email = "technology@rectoryschool.org"
        
        return msg
    
    if operation == 'sample':
        teacher = choice(list(data.keys()))
        msg = generate_message(teacher)
        msg.to = [request.user.email]
        
        django_rq.enqueue(send_msg, msg)
        
        return HttpResponse("Your sample is on the way", content_type="text/plain")
    
    elif operation == 'redirect':
        for teacher in data:
            msg = generate_message(teacher)
            msg.to = [request.user.email]
        
            django_rq.enqueue(send_msg, msg)
        
        return HttpResponse("All {count:} teacher e-mails have been generated and are being redirected to you.".format(count=len(data)), content_type="text/plain")
    
    elif operation == 'send':
        for teacher in data:
            msg = generate_message(teacher)
            confirmation_addresses.extend(msg.to)
            
            django_rq.enqueue(send_msg, msg)
        
        django_rq.enqueue(send_confirmation_email, confirmation_addresses, [request.user.email])
        
        return HttpResponse("All {count:} teacher e-mails have been queued for delivery.".format(count=len(data)), content_type="text/plain")
    
@permission_required('courseevaluations.can_send_emails')
def send_advisor_tutor_status(request):
    try:
        iip_course_numbers = settings.IIP_COURSE_IDS
    except AttributeError:
        iip_course_numbers = []
    
    evaluation_set_id = request.POST['evaluation_set_id']
    operation = request.POST['send_type']
    
    evaluation_set = EvaluationSet.objects.get(pk=evaluation_set_id)
    iip_courses = Course.objects.filter(number__in=iip_course_numbers)
    academic_year = AcademicYear.objects.current()
    
    if not evaluation_set.is_open:
        return HttpResponse("Error: This evaluation set is closed")
    
    evaluables = Evaluable.objects.filter(evaluation_set=evaluation_set).prefetch_related('student')
    students = {}
    
    confirmation_addresses = []
    
    for evaluable in evaluables:
        if evaluable.student not in students:
            students[evaluable.student] = {'complete': [], 'incomplete': []}
        
        if evaluable.complete:
            students[evaluable.student]['complete'].append(evaluable)
        else:
            students[evaluable.student]['incomplete'].append(evaluable)
    
    teacher_student_mapping = {}
    
    for student in students:
        enrollment = Enrollment.objects.get(student=student, academic_year=academic_year)
        advisor = enrollment.advisor
        if not advisor in teacher_student_mapping:
            teacher_student_mapping[advisor] = {}
        
        teacher_student_mapping[advisor][student] = students[student]
        
        iip_registrations = StudentRegistration.objects.filter(section__course__in=iip_courses, student=student, section__academic_year=academic_year)
        for registration in iip_registrations:
            tutor = registration.section.teacher
            if not tutor in teacher_student_mapping:
                teacher_student_mapping[tutor] = {}
            
            teacher_student_mapping[tutor][student] = students[student]
    
    def generate_message(teacher):
        any_incomplete = False
        status_lines = []
        
        for student in sorted(teacher_student_mapping[teacher], key=lambda s: (s.last_name, s.first_name)):
            complete_count = len(teacher_student_mapping[teacher][student]['complete'])
            incomplete_count = len(teacher_student_mapping[teacher][student]['incomplete'])
            total_count = complete_count + incomplete_count
            
            if teacher_student_mapping[teacher][student]['incomplete']:    
                any_incomplete = True
                status_lines.append("{student:}: {complete_count:}/{total_count:} complete".format(student=student.name, complete_count=complete_count, incomplete_count=incomplete_count, total_count=total_count))
            else:
                status_lines.append("{student:}: All complete".format(student=student.name))
        
        msg = EmailMessage()
        msg.to = [teacher.email]
        
        if any_incomplete:
            msg.subject = "Course evaluation status: Incomplete student list"
        else:
            msg.subject = "Course evaluation status: All students completed"

        msg.body = "Evaluation status for the tutees and advisees of {teacher:}:\n\n{status:}".format(status="\n".join(status_lines), teacher=teacher.name)
        msg.from_email = "technology@rectoryschool.org"
        
        return msg
    
    if operation == 'sample':
        teacher = choice(list(teacher_student_mapping.keys()))
        msg = generate_message(teacher)
        msg.to = [request.user.email]
        
        django_rq.enqueue(send_msg, msg)
        
        return HttpResponse("Your sample is on the way", content_type="text/plain")
    
    elif operation == 'redirect':
        for teacher in teacher_student_mapping:
            msg = generate_message(teacher)
            msg.to = [request.user.email]
        
            django_rq.enqueue(send_msg, msg)
        
        return HttpResponse("All {count:} advisor/tutor e-mails have been generated and are being redirected to you.".format(count=len(teacher_student_mapping)), content_type="text/plain")
    
    elif operation == 'send':
        for teacher in teacher_student_mapping:
            msg = generate_message(teacher)
            confirmation_addresses.extend(msg.to)
            
            django_rq.enqueue(send_msg, msg)
        
        django_rq.enqueue(send_confirmation_email, confirmation_addresses, [request.user.email])
        
        return HttpResponse("All {count:} advisor/tutor e-mails have been queued for delivery.".format(count=len(teacher_student_mapping)), content_type="text/plain")