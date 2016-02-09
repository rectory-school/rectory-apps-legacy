from django.shortcuts import render, redirect
from datetime import date, timedelta
from django.conf import settings
from django.http import HttpResponse

from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required, permission_required

from io import StringIO

from enrichmentmanager.models import EnrichmentSlot, Student, Teacher, EnrichmentSignup, EnrichmentOption
from enrichmentmanager.lib import getUnassignedAdvisors, getRoomCounts

def getMonday(d):
    return d - timedelta(days=d.weekday())

@permission_required('enrichmentmanager.can_view_reports')
def index(request):
    slotOptions = EnrichmentSlot.objects.filter(date__gte=date.today()).order_by('date')
    
    weekOptions = {}
    
    for slotOption in slotOptions:
        monday = getMonday(slotOption.date)
        if monday not in weekOptions:
            weekOptions[monday] = []
        
        weekOptions[monday].append(slotOption)
    
    data = {
        'weekOptions': sorted(weekOptions.items()),
    }
    
    return render(request, "enrichmentmanager/reports/index.html", data)

@permission_required('enrichmentmanager.can_view_reports')
def room_counts(request, year, month, day):
    year, month, day = map(int, (year, month, day))
    
    structuredRoomCounts = getRoomCounts(date(year, month, day))
    slots = sorted(structuredRoomCounts.keys(), key=lambda s: s.date)
    
    slotList = []
    
    for slot in structuredRoomCounts:
        roomList = []
        
        for room in structuredRoomCounts[slot]:
            optionList = []
            count = structuredRoomCounts[slot][room]['count']
            options = structuredRoomCounts[slot][room]['options']
            
            for option in options:
                optionList.append((option['option'], option['count']))
            
            optionList.sort(key=lambda o: (o[0].teacher.last_name, o[0].teacher.first_name))
                
            roomList.append((room, count, optionList))
        
        roomList.sort(key=lambda r: r[0])
        
        slotList.append((slot, roomList))
    
    slotList.sort(key=lambda s: s[0].date)    
            
    data = {'roomCounts': slotList, 'slots': slots, 'monday': getMonday(date(year, month, day))}
    
    return render(request, "enrichmentmanager/reports/by_location.html", data)
    
    
@permission_required('enrichmentmanager.can_view_reports')
def email_demo(request):
    template = request.GET.get("template")
    
    if template == "unassigned_advisor":
        data = {'advisor': Teacher.objects.first(), 'count': 5, 'students': Student.objects.all()[:5]}
        return render(request, "enrichmentmanager/emails/unassigned_advisor.html", data)

    if template == "unassigned_administrator":
        unassignedAdvisors = getUnassignedAdvisors(date.today())
        count = sum(len(students) for students in unassignedAdvisors.values())
        data = {'unassignedData': unassignedAdvisors, 'count': count}
        return render(request, 'enrichmentmanager/emails/unassigned_administrator.html', data)
    
    if template == "students_by_enrichment":
        slot = EnrichmentSlot.objects.filter(date__gte=date.today()).order_by('date').first()
    
        slotData = []
    
        lockouts = Student.objects.exclude(lockout="")
    
        #Slot, (option, students), lockouts
        slotRow = (slot, [], lockouts)
    
        slotData.append(slotRow)
    
        q = EnrichmentOption.objects.filter(slot=slot)
        
        for option in q:
            students = option.students.filter(lockout="")
        
            slotRow[1].append((option, students))
    
        return render(request, 'enrichmentmanager/emails/by_enrichment.html', {'slotData': slotData})

@permission_required('enrichmentmanager.can_view_reports')
def by_student(request, year, month, day):
    year, month, day = map(int, (year, month, day))
    monday = getMonday(date(year, month, day))
    sunday = monday + timedelta(days=6)
    
    slots = EnrichmentSlot.objects.filter(date__gte=monday).filter(date__lte=sunday).order_by('date')
    
    response = HttpResponse(content_type="text/plain; charset=utf-8")
    
    for slot in slots:
        response.write("{date}".format(date=slot.date.strftime("%B %d, %Y").center(80, "=")))
        response.write("\n\n")
        
        for student in Student.objects.all():
            try:
                option = EnrichmentSignup.objects.get(slot=slot, student=student).enrichment_option
                response.write("{student}: {location} with {teacher}\n".format(student=student.name, location=option.location, teacher=option.teacher.name))
            except EnrichmentSignup.DoesNotExist:
                response.write("{student}: Unassigned\n".format(student=student.name))
    
    return response

@permission_required('enrichmentmanager.can_view_reports')
def by_enrichment_option(request, year, month, day, teacher=None, dateOnly=False):
    year, month, day = map(int, (year, month, day))
    monday = getMonday(date(year, month, day))
    sunday = monday + timedelta(days=6)
    
    if dateOnly:
        slots = EnrichmentSlot.objects.filter(date=date(year, month, day))
    else:
        slots = EnrichmentSlot.objects.filter(date__gte=monday).filter(date__lte=sunday).order_by('date')
    
    slotData = []
    
    for slot in slots:
        lockouts = Student.objects.exclude(lockout="")
        
        #Slot, (option, students), lockouts
        slotRow = (slot, [], lockouts)
        
        slotData.append(slotRow)
        
        q = EnrichmentOption.objects.filter(slot=slot)
        
        if teacher:
            q = q.filter(teacher=Teacher.objects.get(pk=teacher))
        
        for option in q:
            students = option.students.filter(lockout="")
            
            slotRow[1].append((option, students))
    
    return render(request, 'enrichmentmanager/reports/by_enrichment.html', {'slotData': slotData})

@permission_required('enrichmentmanager.can_view_reports')
def student_printable(request, year, month, day, advisor=None):
    year, month, day = map(int, [year, month, day])
    slot = EnrichmentSlot.objects.get(date=date(year, month, day))
    
    if advisor:
        advisor = Teacher.objects.get(id=advisor)
        students = Student.objects.filter(advisor=advisor)
    else:
        students = Student.objects.all()
    
    studentData = []
    
    for student in students:
        try:
            signup = EnrichmentSignup.objects.get(student=student, slot=slot)
        except EnrichmentSignup.DoesNotExist:
            signup = None
            
        studentData.append((student, signup))
    
    if slot.date > date.today():
        futureWarning = True
    else:
        futureWarning = False
    
    data = {
        'advisor': (advisor or None), 
        'slot': slot, 
        'students': studentData, 
        'backURL': request.GET.get("backURL"), 
        'backTitle': request.GET.get("backTitle"), 
        'futureWarning': futureWarning
    }
    
    return render(request, 'enrichmentmanager/reports/printable_student.html', data)
    

@permission_required('enrichmentmanager.can_view_reports')
def grid(request, year, month, day, unassigned=False):
    year, month, day = map(int, (year, month, day))
    monday = getMonday(date(year, month, day))
    sunday = monday + timedelta(days=6)
    
    slots = EnrichmentSlot.objects.filter(date__gte=monday).filter(date__lte=sunday).order_by('date')
    
    students = Student.objects.all()
    unassignedStudentIDs = set()
    
    if unassigned:
        for student in students:
            if student.id in unassignedStudentIDs:
                continue
        
            if student.lockout:
                continue
        
            for slot in slots:
                try:
                    EnrichmentSignup.objects.get(student=student, slot=slot)
                except EnrichmentSignup.DoesNotExist:
                    unassignedStudentIDs.add(student.id)
    
    if unassigned:
        students = Student.objects.filter(id__in=unassignedStudentIDs)
    else:
        students = Student.objects.all()
    
    byAdvisor = {}
    
    for student in students:
        if not student.advisor in byAdvisor:
            byAdvisor[student.advisor] = []
        
        byAdvisor[student.advisor].append(student)
    
    byAdvisorFlat = []
    for advisor in sorted(byAdvisor.keys(), key=lambda a: (a.last_name, a.first_name)):
        byAdvisorFlat.append((advisor, byAdvisor[advisor]))
    
    
    relatedSignups = {}
    for enrichmentSignup in EnrichmentSignup.objects.filter(slot__in=slots, student__in=students).prefetch_related('student', 'slot'):
        key = "slot_{slot_id}_{student_id}".format(slot_id=enrichmentSignup.slot.id, student_id=enrichmentSignup.student.id)
        relatedSignups[key] = enrichmentSignup.enrichment_option.id
    
    
    data = {'students': students, 
        'byAdvisor': byAdvisorFlat,
        'monday': monday,
        'slots': slots,
        'relatedSignups': relatedSignups
    }
    
    if unassigned:
        data['reportTitle'] = 'Unassigned students'
    else:
        data['reportTitle'] = 'Assignment grid'
    
    return render(request, 'enrichmentmanager/reports/grid.html', data)
