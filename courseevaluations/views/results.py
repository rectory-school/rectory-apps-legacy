#!/usr/bin/python

from io import BytesIO
from zipfile import ZipFile, ZIP_STORED

from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import permission_required

from academics.models import Course, Section, Teacher, Dorm, Grade
from courseevaluations.models import Evaluable, CourseEvaluation, DormParentEvaluation, IIPEvaluation, EvaluationSet, MELPEvaluation

from courseevaluations.lib.results import build_report

@permission_required('courseevaluations.can_view_results')
def zip_teacher_course(request, evaluation_set_id):
    evaluation_set = EvaluationSet.objects.get(pk=evaluation_set_id)
    
    evaluables = CourseEvaluation.objects.filter(evaluation_set=evaluation_set)
    
    by_teacher = {}
    
    for course_evaluation in evaluables:
        teacher = course_evaluation.section.teacher
        course = course_evaluation.section.course
        
        if not teacher in by_teacher:
            by_teacher[teacher] = {}
        
        if not course in by_teacher[teacher]:
            by_teacher[teacher][course] = []
        
        by_teacher[teacher][course].append(course_evaluation)
    
    out = BytesIO()
    with ZipFile(out, mode='w', compression=ZIP_STORED) as zip_file:
        for teacher in by_teacher:
            for course in by_teacher[teacher]:
                evaluables = by_teacher[teacher][course]
                title = "{course:} with {teacher:} ({evaluation_set:})".format(
                    course=course.course_name,
                    teacher=teacher.name,
                    evaluation_set=evaluation_set.name
                    )
                
                
                report_file = BytesIO()
                build_report(report_file, evaluables, title)
                file_name = "{department:}/{last_name:}, {first_name:}/{course:}.pdf".format(
                    department = course.department,
                    last_name = teacher.last_name,
                    first_name=teacher.first_name,
                    course=course.course_name,
                )
                
                zip_file.writestr(file_name, report_file.getvalue())
    
    response = HttpResponse(content_type='application/zip')
    response['Content-Disposition'] = 'filename="Course Evaluations by Department, Teacher, and Course for {evaluation_set:}.zip"'.format(evaluation_set=evaluation_set.name)
    
    response.write(out.getvalue())
    return response

@permission_required('courseevaluations.can_view_results')
def aggregate(request, evaluation_set_id):
    evaluation_set = EvaluationSet.objects.get(pk=evaluation_set_id)
    
    evaluables = CourseEvaluation.objects.filter(evaluation_set=evaluation_set)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report.pdf"'
    
    title = "All evaluations for {evaluation_set:}".format(evaluation_set=evaluation_set.name)
    build_report(response, evaluables, title=title, comments=False)
    return response

@permission_required('courseevaluations.can_view_results')
def grade(request, evaluation_set_id, grade_id):
    evaluation_set = EvaluationSet.objects.get(pk=evaluation_set_id)
    grade = Grade.objects.get(pk=grade_id)
    
    evaluables = CourseEvaluation.objects.filter(
        evaluation_set=evaluation_set, enrollment__grade=grade)
        
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="{grade:} ({evaluation_set:}).pdf"'.format(grade=grade, evaluation_set=evaluation_set.name)
    
    title = "All evaluations for {grade:} ({evaluation_set:})".format(grade=grade, evaluation_set=evaluation_set.name)
    build_report(response, evaluables, title=title, comments=False)
    return response
        
@permission_required('courseevaluations.can_view_results')
def teacher(request, evaluation_set_id, teacher_id):
    teacher = Teacher.objects.get(pk=teacher_id)
    evaluation_set = EvaluationSet.objects.get(pk=evaluation_set_id)
    
    if request.GET.get("unmask_comments") == "1" and request.user.has_perm("courseevaluations.can_unmask_comments"):
        unmask_comments=True
    else:
        unmask_comments=False
    
    evaluables = CourseEvaluation.objects.filter(section__teacher=teacher, evaluation_set=evaluation_set)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report.pdf"'
    
    title = "All evaluations for {teacher:} ({evaluation_set:})".format(
        teacher=teacher.name,
        evaluation_set=evaluation_set.name
        )
    
    build_report(response, evaluables, title=title, unmask_comments=unmask_comments)
    
    return response

@permission_required('courseevaluations.can_view_results')
def teacher_course(request, evaluation_set_id, teacher_id, course_id):
    course = Course.objects.get(pk=course_id)
    teacher = Teacher.objects.get(pk=teacher_id)
    evaluation_set = EvaluationSet.objects.get(pk=evaluation_set_id)
    
    if request.GET.get("unmask_comments") == "1" and request.user.has_perm("courseevaluations.can_unmask_comments"):
        unmask_comments=True
    else:
        unmask_comments=False
    
    sections = Section.objects.filter(course=course, teacher=teacher)
    
    evaluables = CourseEvaluation.objects.filter(section__in=sections, evaluation_set=evaluation_set)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report.pdf"'
    
    title = "{course:} with {teacher:} ({evaluation_set:})".format(
        course=course.course_name,
        teacher=teacher.name,
        evaluation_set=evaluation_set.name
        )
    
    build_report(response, evaluables, title=title, unmask_comments=unmask_comments)
    
    return response

@permission_required('courseevaluations.can_view_results')
def section(request, evaluation_set_id, section_id):
    section = Section.objects.get(pk=section_id)
    evaluation_set = EvaluationSet.objects.get(pk=evaluation_set_id)
    
    if request.GET.get("unmask_comments") == "1" and request.user.has_perm("courseevaluations.can_unmask_comments"):
        unmask_comments=True
    else:
        unmask_comments=False
        
    evaluables = CourseEvaluation.objects.filter(section=section, evaluation_set=evaluation_set)
    
    response = HttpResponse(content_type='application/pdf')
    
    title = "{course:}: {section:} with {teacher:} ({evaluation_set:})".format(
        course = section.course.course_name,
        section=section.csn,
        teacher=section.teacher.name,
        evaluation_set=evaluation_set.name
        )
    
    build_report(response, evaluables, title=title, unmask_comments=unmask_comments)
    
    return response

@permission_required('courseevaluations.can_view_results')
def iip(request, evaluation_set_id, teacher_id):
    evaluation_set = EvaluationSet.objects.get(pk=evaluation_set_id)
    teacher = Teacher.objects.get(pk=teacher_id)
    
    if request.GET.get("unmask_comments") == "1" and request.user.has_perm("courseevaluations.can_unmask_comments"):
        unmask_comments=True
    else:
        unmask_comments=False
    
    evaluables = IIPEvaluation.objects.filter(evaluation_set=evaluation_set, teacher=teacher)
    
    response = HttpResponse(content_type='application/pdf')
    
    title = "IIP with {teacher:} ({evaluation_set:})".format(
        teacher=teacher.name,
        evaluation_set=evaluation_set.name
        )
    
    build_report(response, evaluables, title=title, unmask_comments=unmask_comments)
    
    return response

@permission_required('courseevaluations.can_view_results')
def zip_iip(request, evaluation_set_id):
    evaluation_set = EvaluationSet.objects.get(pk=evaluation_set_id)
    
    evaluables = IIPEvaluation.objects.filter(evaluation_set=evaluation_set)
    
    by_teacher = {}
    
    for iip_evaluation in evaluables:
        teacher = iip_evaluation.teacher
        
        if not teacher in by_teacher:
            by_teacher[teacher] = []
        
        by_teacher[teacher].append(iip_evaluation)
    
    out = BytesIO()
    with ZipFile(out, mode='w', compression=ZIP_STORED) as zip_file:
        for teacher in by_teacher:
            evaluables = by_teacher[teacher]
            title = "IIP with {teacher:} ({evaluation_set:})".format(
                teacher=teacher.name,
                evaluation_set=evaluation_set.name
                )
            
            
            report_file = BytesIO()
            build_report(report_file, evaluables, title)
            file_name = "{last_name:}, {first_name:}.pdf".format(
                last_name = teacher.last_name,
                first_name=teacher.first_name,
            )
            
            zip_file.writestr(file_name, report_file.getvalue())
    
    response = HttpResponse(content_type='application/zip')
    response['Content-Disposition'] = 'filename="IIP Evaluations by Teacher for {evaluation_set:}.zip"'.format(evaluation_set=evaluation_set.name)
    
    response.write(out.getvalue())
    return response

@permission_required('courseevaluations.can_view_results')
def dorm_parent_dorm_parent(request, evaluation_set_id, dorm_id, parent_id):
    evaluation_set = EvaluationSet.objects.get(pk=evaluation_set_id)
    dorm = Dorm.objects.get(pk=dorm_id)
    parent = Teacher.objects.get(pk=parent_id)
    
    if request.GET.get("unmask_comments") == "1" and request.user.has_perm("courseevaluations.can_unmask_comments"):
        unmask_comments=True
    else:
        unmask_comments=False
    
    evaluables = DormParentEvaluation.objects.filter(evaluation_set=evaluation_set, dorm=dorm, parent=parent)
    
    response = HttpResponse(content_type='application/pdf')
    
    title = "{dorm:} with {parent:} ({evaluation_set:})".format(
        dorm = str(dorm),
        parent=parent.name,
        evaluation_set=evaluation_set.name
        )
    
    build_report(response, evaluables, title=title, unmask_comments=unmask_comments)
    
    return response

@permission_required('courseevaluations.can_view_results')
def dorm_parent_dorm(request, evaluation_set_id, dorm_id):
    evaluation_set = EvaluationSet.objects.get(pk=evaluation_set_id)
    dorm = Dorm.objects.get(pk=dorm_id)
    
    if request.GET.get("unmask_comments") == "1" and request.user.has_perm("courseevaluations.can_unmask_comments"):
        unmask_comments=True
    else:
        unmask_comments=False
    
    evaluables = DormParentEvaluation.objects.filter(evaluation_set=evaluation_set, dorm=dorm)
    
    response = HttpResponse(content_type='application/pdf')
    
    title = "Dorm Parent Evaluation for {dorm:} ({evaluation_set:})".format(
        dorm = str(dorm),
        evaluation_set=evaluation_set.name
        )
    
    build_report(response, evaluables, title=title, unmask_comments=unmask_comments)
    
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
def zip_dorm_parent_dorm_dorm_parent(request, evaluation_set_id):
    evaluation_set = EvaluationSet.objects.get(pk=evaluation_set_id)
    
    evaluables = DormParentEvaluation.objects.filter(evaluation_set=evaluation_set)
    
    by_dorm = {}
    
    for dorm_parent_evaluation in evaluables:
        dorm = dorm_parent_evaluation.dorm
        parent = dorm_parent_evaluation.parent
        
        if not dorm in by_dorm:
            by_dorm[dorm] = {}
        
        if not parent in by_dorm[dorm]:
            by_dorm[dorm][parent] = []
        
        by_dorm[dorm][parent].append(dorm_parent_evaluation)
    
    out = BytesIO()
    with ZipFile(out, mode='w', compression=ZIP_STORED) as zip_file:
        for dorm in by_dorm:
            for parent in by_dorm[dorm]:
                evaluables = by_dorm[dorm][parent]
                title = "{dorm:} with {parent:} ({evaluation_set:})".format(
                    dorm = str(dorm),
                    parent=parent.name,
                    evaluation_set=evaluation_set.name
                    )
                
                report_file = BytesIO()
                build_report(report_file, evaluables, title)
                file_name = "{dorm:}/{last_name:}, {first_name:}.pdf".format(
                    dorm = str(dorm),
                    last_name = parent.last_name,
                    first_name=parent.first_name,
                )
                
                zip_file.writestr(file_name, report_file.getvalue())
    
    response = HttpResponse(content_type='application/zip')
    response['Content-Disposition'] = 'filename="Dorm Evaluations by Dorm and Parent for {evaluation_set:}.zip"'.format(evaluation_set=evaluation_set.name)
    
    response.write(out.getvalue())
    return response

@permission_required('courseevaluations.can_view_results')
def melp_section(request, evaluation_set_id, section_id):
    section = Section.objects.get(pk=section_id)
    evaluation_set = EvaluationSet.objects.get(pk=evaluation_set_id)

    if request.GET.get("unmask_comments") == "1" and request.user.has_perm("courseevaluations.can_unmask_comments"):
        unmask_comments=True
    else:
        unmask_comments=False
    
    evaluables = MELPEvaluation.objects.filter(section=section, evaluation_set=evaluation_set)

    response = HttpResponse(content_type='application/pdf')

    title = "{melp_name:} ({evaluation_set:})".format(
        melp_name=section.course_name,
        evaluation_set=evaluation_set.name
        )

    build_report(response, evaluables, title=title, unmask_comments=unmask_comments)

    return response

@permission_required('courseevaluations.can_view_results')
def melp_aggregate(request, evaluation_set_id):
    evaluation_set = EvaluationSet.objects.get(pk=evaluation_set_id)

    if request.GET.get("unmask_comments") == "1" and request.user.has_perm("courseevaluations.can_unmask_comments"):
        unmask_comments=True
    else:
        unmask_comments=False
    
    evaluables = MELPEvaluation.objects.filter(evaluation_set=evaluation_set)

    response = HttpResponse(content_type='application/pdf')

    title = "Aggregate MELP Results ({evaluation_set:})".format(
        evaluation_set=evaluation_set.name
        )

    build_report(response, evaluables, title=title, unmask_comments=unmask_comments)

    return response



@permission_required('courseevaluations.can_view_results')
def melp_section_zip(request, evaluation_set_id):
    evaluation_set = EvaluationSet.objects.get(pk=evaluation_set_id)
    
    evaluables = MELPEvaluation.objects.filter(evaluation_set=evaluation_set)
    
    by_melp = {}
    
    for melp_evaluation in evaluables:
        section = melp_evaluation.section
        
        if not section in by_melp:
            by_melp[section] = []
        
        by_melp[section].append(melp_evaluation)
    
    out = BytesIO()
    with ZipFile(out, mode='w', compression=ZIP_STORED) as zip_file:
        for melp in by_melp:
            evaluables = by_melp[melp]
            title = "{melp:} ({evaluation_set:})".format(
                melp = melp.course_name,
                evaluation_set=evaluation_set.name
                )
            
            
            report_file = BytesIO()
            build_report(report_file, evaluables, title)
            file_name = "{melp:}.pdf".format(
                melp = melp.course_name,
            )
            
            zip_file.writestr(file_name, report_file.getvalue())
    
    response = HttpResponse(content_type='application/zip')
    response['Content-Disposition'] = 'filename="MELP Evaluations for {evaluation_set:}.zip"'.format(evaluation_set=evaluation_set.name)
    
    response.write(out.getvalue())
    return response


@permission_required('courseevaluations.can_view_results')
def index(request, evaluation_set_id):
    evaluation_set = EvaluationSet.objects.get(pk=evaluation_set_id)
    
    course_evaluables = CourseEvaluation.objects.filter(evaluation_set=evaluation_set)
    dorm_parent_evaluables = DormParentEvaluation.objects.filter(evaluation_set=evaluation_set)
    iip_evaluables = IIPEvaluation.objects.filter(evaluation_set=evaluation_set)
    melp_evaluables = MELPEvaluation.objects.filter(evaluation_set=evaluation_set)
    
    sections = Section.objects.filter(courseevaluation__in=course_evaluables).distinct()
    iip_teachers = Teacher.objects.filter(iipevaluation__in=iip_evaluables).order_by('last_name', 'first_name').distinct()
    melp_sections = Section.objects.filter(melpevaluation__in=melp_evaluables).order_by('course_name').distinct()
    
    used_grade_ids = course_evaluables.values_list('enrollment__grade', flat=True).order_by().distinct()
    
    grades = Grade.objects.filter(pk__in=used_grade_ids)
    
    dorm_parents = []
    for evaluable in dorm_parent_evaluables:
        d = {'dorm': evaluable.dorm, 'parent': evaluable.parent}
        if not d in dorm_parents:
            dorm_parents.append(d)
    
    return render(request, "courseevaluations/results/index.html", {'evaluation_set': evaluation_set, 'sections': sections, 'iip_teachers': iip_teachers, 'dorm_parents': dorm_parents, 'grades': grades, 'melp_sections': melp_sections})