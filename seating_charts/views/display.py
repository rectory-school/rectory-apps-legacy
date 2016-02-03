#!/usr/bin/python

import json
import re
import time

from datetime import date
from cStringIO import StringIO

from django.http import HttpResponse
from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import render

from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.units import inch
from reportlab.lib.utils import simpleSplit
from reportlab.platypus import BaseDocTemplate, Frame, Paragraph, PageBreak, PageTemplate, FrameBreak, NextPageTemplate
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas

from seating import models

FONT="Helvetica"
BOLDFONT="Helvetica-Bold"

@permission_required('seating.view')
def index(request):
    mealTimes = models.MealTime.objects.all()
    layouts = models.Layout.objects.all()
    
    return render(request, 'seating/index.html', {'mealTimes': mealTimes, 'layouts': layouts})

@permission_required('seating.view')
def seatingChartByTable(request, id):
    mealTime = models.MealTime.objects.get(pk=id)
    
    allStudents = set(mealTime.allStudents())
    seenStudents = set()
    
    #Dict of [(Student first, Student last, waiter)]
    
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
        
        students[table].append((student.first_name, student.last_name, False))
        seenStudents.add(student)
    
    
    leftovers = [(s.first_name, s.last_name) for s in (allStudents - seenStudents)]
    leftovers.sort(key=lambda s: (s[1], s[0]))
    
    for t in tables:
        students[t].sort(key=lambda s: (s[1], s[0]))
    
    tables.sort(key=lambda t: natural_keys(t.description))
    
    data = []
    for t in tables:
        d = dict()
        d['table'] = t
        d['students'] = students[t]
        d['fillers'] = fillers[t]
        data.append(d)
    
    return render(request, 'seating/seating_chart_by_table.html', {'leftovers': leftovers, 'tables': data})

@permission_required('seating.view')
def seatingChartByStudent(request, id):
    mealTime = models.MealTime.objects.get(pk=id)

    allStudents = set(mealTime.allStudents())
    seenStudents = set()

    data = []

    for tableAssignment in mealTime.tableassignment_set.all():
        table = tableAssignment.table
        student = tableAssignment.student

        data.append((student.first_name, student.last_name, table.description))

        seenStudents.add(student)

    leftovers = [(s.first_name, s.last_name) for s in (allStudents - seenStudents)]
    leftovers.sort(key=lambda s: (s[1], s[0]))
    data.sort(key=lambda s: (s[1], s[0]))
        
    normal = getSampleStyleSheet()["Normal"]
    heading = getSampleStyleSheet()["Title"]
    heading.fontSize = 40
    
    story=[]
    story.append(Paragraph(mealTime.name, heading))
    story.append(FrameBreak())
    story.append(NextPageTemplate("twoCol"))
    
    for first, last, table in data:
        story.append(Paragraph("%s %s: %s" % (first, last, table), normal))
    
    out = StringIO()
    doc = BaseDocTemplate(out)
    
    top = Frame(doc.leftMargin, doc.height, doc.width, 100)
    frame1 = Frame(doc.leftMargin, doc.bottomMargin, doc.width/2-6, doc.height-75, id='col1')
    frame2 = Frame(doc.leftMargin+doc.width/2+6, doc.bottomMargin, doc.width/2-6, doc.height-75, id='col2')
    doc.addPageTemplates([PageTemplate(id='topColHeader',frames=[top, frame1,frame2]), ])
    
    frame1 = Frame(doc.leftMargin, doc.bottomMargin, doc.width/2-6, doc.height, id='col1')
    frame2 = Frame(doc.leftMargin+doc.width/2+6, doc.bottomMargin, doc.width/2-6, doc.height, id='col2')
    doc.addPageTemplates([PageTemplate(id='twoCol',frames=[frame1,frame2]), ])
    
    #start the construction of the pdf
    doc.build(story)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="Seating chart {mealTime:}.pdf"'.format(mealTime=mealTime.name)

    response.write(out.getvalue())

    return response

@permission_required('seating.view')
def seatingChartInsert(request, id):
    layout = models.Layout.objects.get(pk=id)
    
    out = StringIO()
    
    c = canvas.Canvas(out, pagesize=(6*inch, 4*inch))
    
    #Only one
    if not layout.right_print:
        mealTime = layout.left_print
        
        tables = mealTime.table_set.all()
        
        for table in tables:
            c.setFontSize(20)
            c.drawCentredString(3*inch, 3.65*inch, table.description)
            assignments = models.TableAssignment.objects.filter(meal_time=mealTime, table=table)
            students = models.Student.objects.filter(tableassignment__in=assignments)
            fillers = models.SeatFiller.objects.filter(meal_time=mealTime, table=table)
            
            drawMeal(c, x=.25*inch, y=(4-.6)*inch, width=5.5*inch, height=3.5*inch, mealTime=mealTime, fillers=fillers, students=students)
            c.setFontSize(8)
            c.setFillColor(colors.grey)
            c.drawRightString((6-.25)*inch, .25*inch, date.today().strftime("%Y-%m-%d"))
            c.showPage()
    
    #Double layout
    else:
        tables = set(layout.left_print.table_set.all()) | set(layout.right_print.table_set.all())
        
        for table in tables:
            c.setFontSize(20)
            c.drawCentredString(3*inch, 3.65*inch, table.description)
            
            #Left
            mealTime = layout.left_print
            assignments = models.TableAssignment.objects.filter(meal_time=mealTime, table=table)
            students = models.Student.objects.filter(tableassignment__in=assignments)
            fillers = models.SeatFiller.objects.filter(meal_time=mealTime, table=table)
            drawMeal(c, x=.25*inch, y=(4-.7)*inch, width=2.5*inch, height=3.3*inch, mealTime=mealTime, fillers=fillers, students=students)
            
            #Line
            c.line(3*inch, .25*inch, 3*inch, (4-.7)*inch)
            
            #Right
            mealTime = layout.right_print
            assignments = models.TableAssignment.objects.filter(meal_time=mealTime, table=table)
            students = models.Student.objects.filter(tableassignment__in=assignments)
            fillers = models.SeatFiller.objects.filter(meal_time=mealTime, table=table)
            drawMeal(c, x=3.25*inch, y=(4-.7)*inch, width=2.75*inch, height=3.3*inch, mealTime=mealTime, fillers=fillers, students=students)
            
            c.setFontSize(8)
            c.setFillColor(colors.grey)
            c.drawRightString((6-.25)*inch, .25*inch, date.today().strftime("%Y-%m-%d"))
            c.showPage()
            
            
    
    c.save()
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="Seating chart.pdf"'
    
    response.write(out.getvalue())
    return response
    

def drawMeal(c, x, y, width, height, mealTime, fillers, students):
    xCenter = x + width / 2
    
    c.setFillColor(colors.black)
    c.setFontSize(16)
    c.drawCentredString(xCenter, y, mealTime.name)
    y -= 16
    
    c.setFontSize(12)
    for f in fillers:
        if f.display:
            c.drawCentredString(xCenter, y, f.description)
            y -= 12
    
    if fillers:
        y -= 10
        
    for s in students:
        name = s.flaggedName
        lines = simpleSplit(name, FONT, 12, width)
        
        if len(lines) == 1:
            c.drawString(x, y, lines[0])
        else:
            c.drawString(x, y, lines[0])
            
            for line in lines[1:]:
                y -= 12
                c.drawString(x+12, y, line)
        
        c.setFontSize(12)
                                
        y -= 14
    
    return y

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    '''
    return [ atoi(c) for c in re.split('(\d+)', text) ]