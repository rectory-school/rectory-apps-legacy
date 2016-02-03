#!/usr/bin/python

import json
import re
import time

from datetime import date

from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.db import transaction
from django.contrib.auth.decorators import permission_required, login_required

from seating import models

from seating.lib import getTables, GeneratorError

@permission_required('seating.edit')
def seatingChartEditor(request, id):
    mealTime = models.MealTime.objects.get(pk=id)
    
    return render(request, 'seating/seating_chart_editor.html', {'mealTime': mealTime})

@permission_required('seating.edit')
def shuffle(request, id):
    mealTime = models.MealTime.objects.get(pk=id)
    
    models.TableAssignment.objects.filter(meal_time=mealTime).delete()
    
    with transaction.atomic():
        try:
            for table in getTables(mealTime):
                for student in table.students:
                    ta = models.TableAssignment()
                    ta.student = models.Student.objects.get(pk=student.id)
                    ta.table = models.Table.objects.get(pk=table.id)
                    ta.meal_time = mealTime
                    ta.save()

        except GeneratorError as e:
            return HttpResponse("Error generating seating chart:\n%s" % e, content_type="text/plain")
    
    return HttpResponseRedirect(reverse('seating_chart_editor', kwargs={'id': mealTime.id}))
    

@permission_required('seating.edit')
def seatingChartData(request, id):
    mealTime = models.MealTime.objects.get(pk=id)
    allStudents = set(mealTime.allStudents())
    seenStudents = set()
    
    students = {}
    fillers = {}
    tables = []
    
    for table in mealTime.table_set.all():
        students[table] = []
        fillers[table] = []
        tables.append(table)
         
        tableFillers = models.SeatFiller.objects.filter(table=table, meal_time=mealTime)
        
        for f in tableFillers:
            fillers[table].append(f)
        
    for tableAssignment in mealTime.tableassignment_set.all():
        table = tableAssignment.table
        student = tableAssignment.student
        
        students[table].append(student)
        seenStudents.add(student)
    
    
    
    leftovers = [s for s in (allStudents - seenStudents)]
    leftovers.sort(key=lambda s: (s.last_name, s.first_name))
    
    for t in tables:
        students[t].sort(key=lambda s: (s.last_name, s.first_name))
    
    tables.sort(key=lambda t: natural_keys(t.description))
    
    out = {'tables': [], 'leftovers': []}
    
    def studentToDict(student):
        return {'first_name': student.first_name, 
            'last_name': student.last_name, 
            'id': student.id, 
            'gender': student.gender.gender, 
            'ethnicity': student.ethnicity.ethnicity,
            'grade': student.grade.grade}
        
    def fillerToDict(filler):
        return {'description': filler.description,
        'id': filler.id,
        'seats': filler.seats}
        
    def tableToDict(table):
        return {'description': table.description,
        'id': table.id,
        'capacity': table.capacity}
    
    for t in tables:        
        d = tableToDict(t)
        d['students'] = map(studentToDict, students[t])
        d['fillers'] = map(fillerToDict, fillers[t])
        
        out['tables'].append(d)
        
    out['leftovers'] = map(studentToDict, leftovers)
        
    return JsonResponse(out)

@permission_required('seating.edit')
def moveStudent(request, id):
    studentID = request.POST["student_id"]
    newTableID = request.POST.get("table_id", None)
    
    mealTime = models.MealTime.objects.get(pk=id)
    
    student = models.Student.objects.get(pk=studentID)
    
    with transaction.atomic():
        models.TableAssignment.objects.filter(student=student, meal_time=mealTime).delete()
        
        if newTableID:
            tableAssignment = models.TableAssignment()
            tableAssignment.meal_time = mealTime
            tableAssignment.student = student
            tableAssignment.table = models.Table.objects.get(pk=newTableID)
            tableAssignment.save()
    
    return HttpResponse("OK")

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    '''
    return [ atoi(c) for c in re.split('(\d+)', text) ]