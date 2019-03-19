#!/usr/bin/python

from academics.models import Student, Section
from courseevaluations.models import CourseEvaluation, IIPEvaluation, DormParentEvaluation

def get_incomplete_evaluables_by_teacher(evaluation_set):
    course_evaluables = CourseEvaluation.objects.filter(evaluation_set=evaluation_set, complete=False)
    iip_evaluables = IIPEvaluation.objects.filter(evaluation_set=evaluation_set, complete=False)
    dorm_parent_evaluables = DormParentEvaluation.objects.filter(evaluation_set=evaluation_set, complete=False)
    
    data = {}
    
    for evaluable in course_evaluables:
        section = evaluable.section
        course = section.course
        teacher = section.teacher
        student = evaluable.student
        
        if not teacher in data:
            data[teacher] = {}
        
        if not 'course' in data[teacher]:
            data[teacher]['course'] = {}
            
        if not section in data[teacher]['course']:
            data[teacher]['course'][section] = []
        
        data[teacher]['course'][section].append(student)
    
    for evaluable in iip_evaluables:
        teacher = evaluable.teacher
        student = evaluable.student
                
        if not teacher in data:
            data[teacher] = {}
        
        if not 'iip' in data[teacher]:
            data[teacher]['iip'] = []
        
        data[teacher]['iip'].append(student)
    
    for evaluable in dorm_parent_evaluables:
        teacher = evaluable.parent
        dorm = evaluable.dorm
        student = evaluable.student
                
        if not teacher in data:
            data[teacher] = {}
        
        if not 'dorm' in data[teacher]:
            data[teacher]['dorm'] = {}
        
        if not dorm in data[teacher]['dorm']:
            data[teacher]['dorm'][dorm] = []
            
        data[teacher]['dorm'][dorm].append(student)
    
    return data

def flatten_evaluables_by_teacher(data):
    flattened_data = []
    for teacher in sorted(data.keys(), key=lambda t: t and (t.last_name, t.first_name) or ("", "")):
        section_row = []
        flattened_data.append((teacher, section_row))
        
        if 'course' in data[teacher]:
            for section in sorted(data[teacher]['course'].keys(), key=lambda sec: (sec.course.course_name, sec.csn)):
                student_row = sorted(data[teacher]['course'][section], key=lambda stu: (stu.last_name, stu.first_name))
                section_row.append(("{course:}: {csn:}".format(course=section.course.course_name, csn=section.csn), student_row))
        
        if 'iip' in data[teacher]:
            student_row = sorted(data[teacher]['iip'], key=lambda stu: (stu.last_name, stu.first_name))
            section_row.append(("IIP", student_row))
        
        if 'dorm' in data[teacher]:
            for dorm in sorted(data[teacher]['dorm'].keys(), key=lambda d: (str(d))):
                student_row = sorted(data[teacher]['dorm'][dorm], key=lambda stu: (stu.last_name, stu.first_name))
                section_row.append((str(dorm), student_row))
                
    return flattened_data