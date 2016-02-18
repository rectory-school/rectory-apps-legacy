from django.shortcuts import render, redirect
from datetime import date, timedelta
from django.conf import settings

from django.db.models import Max, Min
from django.contrib.auth.models import User
from django.db.transaction import atomic
from django.core.exceptions import ValidationError, PermissionDenied
from django.core.urlresolvers import reverse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Min

from enrichmentmanager.models import EnrichmentSlot, Student, Teacher, EnrichmentSignup, EnrichmentOption
from enrichmentmanager.lib import getMonday, canEditSignup

import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

def parseDate(s):
    year, month, day = map(int, s.split("-"))
    return date(year, month, day)

@permission_required("enrichmentmanager.can_view_own_advisees", login_url='/google_auth/login/')
def index(request):
    currentUser = request.user
    
    try:
        advisor = Teacher.objects.get(academic_teacher__email=currentUser.email)
    except Teacher.DoesNotExist:
        return HttpResponse("Error: Teacher object does not exist for '{:}'. Please contact Technology.".format(currentUser.email))
    
    try:
        slotToday = EnrichmentSlot.objects.get(date=date.today())
    except EnrichmentSlot.DoesNotExist:
        slotToday = None
    
    if slotToday and Student.objects.filter(advisor=advisor).count():
        adviseeQuickReport = reverse('reporting_student_printable', kwargs={'year': date.today().year, 'month': date.today().month, 'day': date.today().day, 'advisor': advisor.id})
    else:
        adviseeQuickReport = None
    
    if slotToday:
        try:
            optionToday = EnrichmentOption.objects.get(teacher=advisor, slot=slotToday)
        except EnrichmentOption.DoesNotExist:
            optionToday = None
        
        advisees = []
        for advisee in Student.objects.filter(advisor=advisor):
            try:
                signup = EnrichmentSignup.objects.get(student=advisee, slot=slotToday)
                advisees.append((advisee, "{name:} in {location:}".format(name=signup.enrichment_option.teacher.name, location=signup.enrichment_option.location)))
                
            except EnrichmentSignup.DoesNotExist:
                advisees.append((advisee, "Unassigned. Please contact the education office"))
                
    else:
        optionToday = None
        advisees = []
    
    if slotToday and EnrichmentOption.objects.filter(teacher=advisor).count() > 0:
        teacherQuickReport = reverse('reporting_by_enrichment_option', kwargs={'year': date.today().year, 'month': date.today().month, 'day': date.today().day, 'teacher': advisor.id})
    else:
       teacherQuickReport = None 
       
    return render(request, "enrichmentmanager/index.html", {'adviseeQuickReport': adviseeQuickReport, 'teacherQuickReport': teacherQuickReport, 'optionToday': optionToday, 'advisees': advisees, 'currentAdvisor': advisor})

@require_http_methods(['POST'])
def save_assignments(request):    
    with atomic():
        #Run new session creation first
        for key in request.POST:
            parts = key.split("_")
            if len(parts) != 4:
                continue
            
            slotID, studentID, keyType = parts[1:]
            
            if keyType == 'option':             
                value = request.POST[key]
                    
                slot = EnrichmentSlot.objects.get(pk=slotID)
                student = Student.objects.get(pk=studentID)

                if not canEditSignup(request.user, slot, student):
                    raise PermissionDenied()
                
                if value:
                    try:
                        option = EnrichmentOption.objects.get(pk=value)
                    except EnrichmentOption.DoesNotExist:
                        logger.error("Enrichment option session {id:} not found".format(id=value))
                        option = None
                else:
                    option = None
                
                #If we're clearing the signup, just delete all possible matching objects
                if not option:
                    EnrichmentSignup.objects.filter(slot=slot, student=student).delete()
                
                #Find and update the existing signup if it exists, otherwide create one
                else:                    
                    try:
                        signup = EnrichmentSignup.objects.get(slot=slot, student=student)
                        
                    except EnrichmentSignup.DoesNotExist:
                        signup = EnrichmentSignup(student=student, slot=slot)
                    
                    signup.enrichment_option = option
                    signup.save()
        
        #Do it again, now that our signups should have been reconciled
        for key in request.POST:
            parts = key.split("_")
            if len(parts) != 4:
                continue
            
            slotID, studentID, keyType = parts[1:]
            
            if keyType == 'adminlock':
                value = request.POST[key]
            
                slot = EnrichmentSlot.objects.get(pk=slotID)
                student = Student.objects.get(pk=studentID)
                
                if not canEditSignup(request.user, slot, student):
                    raise PermissionDenied()
                
                if not request.user.has_perm("enrichmentmanager.can_set_admin_lock"):
                    raise PermissionDenied()
                
                try:
                    signup = EnrichmentSignup.objects.get(slot=slot, student=student)
            
                    if value.lower() in ("1", "true"):
                        value = True
                    elif value.lower() in ("0", "false"):
                        value = False
                
                    signup.admin_lock = value
                    signup.save()

                except EnrichmentSignup.DoesNotExist:
                    logger.error("Setting a lock on a non-existent enrichment signup")

    return redirect(request.POST["next"])

def getTemplateData(request, advisor, unassigned, monday):
    sunday = monday + timedelta(days=6)
    
    slots = EnrichmentSlot.objects.filter(date__gte=monday).filter(date__lte=sunday).order_by('date')
    
    if advisor:
        students = Student.objects.filter(advisor=advisor)
    else:
        students = Student.objects.all()
    
    #This can probably be done directly on the DB server
    if unassigned:
        unassignedStudentIDs = set()
        
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
        
        #This is ineffecient, but it guarantees that I get a QuerySet back out, as opposed to working on a list later on
        students = Student.objects.filter(id__in=unassignedStudentIDs)
    
    students = students.order_by('academic_student__last_name', 'academic_student__first_name')
    
    slotChoices = {}
    for slot in slots:
        slotChoices[slot] = EnrichmentOption.objects.filter(slot=slot).prefetch_related('teacher').order_by('teacher__academic_teacher__last_name', 'teacher__academic_teacher__first_name').all()
    
    #This is an extra query if we're grabbing the unassigned set    
    relatedSignups = {}
    for enrichmentSignup in EnrichmentSignup.objects.filter(slot__in=slots, student__in=students).prefetch_related('student', 'slot'):
        key = "slot_{slot_id}_{student_id}".format(slot_id=enrichmentSignup.slot.id, student_id=enrichmentSignup.student.id)
        relatedSignups[key] = enrichmentSignup.enrichment_option.id
    
    slotOptions = EnrichmentSlot.objects.filter(date__gte=date.today())
    weekOptions = set()
    
    for slotOption in slotOptions:
        weekOptions.add(getMonday(slotOption.date))
    
    data = {
        'currentDate': date(monday.year, monday.month, monday.day),
        'slots': slots,
        'students': students,
        'advisors': Teacher.objects.exclude(student=None).order_by('academic_teacher__last_name', 'academic_teacher__first_name').all(),
        'weekOptions': sorted(weekOptions),
        'currentAdvisor': advisor,
        'slotChoices': slotChoices,
        'relatedSignups': relatedSignups,
    }
    
    return data

@permission_required("enrichmentmanager.can_view_own_advisees")    
def advisor_quick(request):
    #Get our next date
    nextDate = EnrichmentSlot.objects.filter(date__gte=date.today()).aggregate(Min('date'))['date__min']
    monday = getMonday(nextDate)
    sunday = monday + timedelta(days=6)
    
    currentUser = request.user
    
    #TODO: Handle case of advisor not found
    advisor = Teacher.objects.get(academic_teacher__email=currentUser.email)
    
    templateData = getTemplateData(request, advisor=advisor, unassigned=False, monday=monday)
    
    return render(request, "enrichmentmanager/assign_advisor.html", templateData)


def advisor_explicit(request, advisor, year, month, day):
    year, month, day = map(int, (year, month, day))
    monday = getMonday(date(year, month, day))
    sunday = monday + timedelta(days=6)
    
    if not request.user.is_authenticated():
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    
    advisor = Teacher.objects.get(pk=advisor)
    
    if request.user.email == advisor.email and request.user.has_perm("enrichmentmanager.can_view_own_advisees"):
        templateData = getTemplateData(request, advisor=advisor, unassigned=False, monday=monday)
        return render(request, "enrichmentmanager/assign_advisor.html", templateData)
    
    elif request.user.has_perm("enrichmentmanager.can_view_other_advisees"):
        templateData = getTemplateData(request, advisor=advisor, unassigned=False, monday=monday)
        return render(request, "enrichmentmanager/assign_advisor.html", templateData)
    
    return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        

@permission_required("enrichmentmanager.can_view_all_advisees")
def unassigned_quick(request):
    monday = getMonday(date.today())
    sunday = monday + timedelta(days=6)
    
    templateData = getTemplateData(request, advisor=None, unassigned=True, monday=monday)
    
    return render(request, "enrichmentmanager/assign_unassigned.html", templateData)

@permission_required("enrichmentmanager.can_view_all_advisees")
def unassigned_explicit(request, year, month, day):
    year, month, day = map(int, (year, month, day))
    monday = getMonday(date(year, month, day))
    sunday = monday + timedelta(days=6)
    
    templateData = getTemplateData(request, advisor=None, unassigned=True, monday=monday)
    
    return render(request, "enrichmentmanager/assign_unassigned.html", templateData)

@permission_required("enrichmentmanager.can_view_single_student")
def single_student(request, student_id, weekday=None):
    slots = EnrichmentSlot.objects.filter(date__gte=date.today())
    student = Student.objects.get(pk=student_id)
    allTeachers = Teacher.objects.exclude(default_room = "").order_by('academic_teacher__last_name', 'academic_teacher__first_name').all()
    
    weekdays = set()
    
    #Initial iteration to get all elegible weekdays
    for slot in slots:
        weekdays.add(slot.date.weekday())
    
    if weekday:
        slots = [s for s in slots if s.date.weekday() == int(weekday)]
    
    relatedSignups = {}
    slotChoices = {}
    
    if slots:    
        for enrichmentSignup in EnrichmentSignup.objects.filter(slot__in=slots, student=student).prefetch_related('student', 'slot'):
            key = "slot_{slot_id}_{student_id}".format(slot_id=enrichmentSignup.slot.id, student_id=enrichmentSignup.student.id)
            relatedSignups[key] = enrichmentSignup.enrichment_option.id
    
        for slot in slots:
            slotChoices[slot] = EnrichmentOption.objects.filter(slot=slot).prefetch_related('teacher').order_by('teacher__academic_teacher__last_name', 'teacher__academic_teacher__first_name').all()
    
    return render(request, "enrichmentmanager/assign_single.html", {'slots': slots, 'student': student, 'relatedSignups': relatedSignups, 'slotChoices': slotChoices, 'weekdays': weekdays, 'allTeachers': allTeachers})
    
@permission_required("enrichmentmanager.can_view_all_advisees")    
def all_quick(request):
    monday = getMonday(date.today())
    sunday = monday + timedelta(days=6)
    
    templateData = getTemplateData(request, advisor=None, unassigned=False, monday=monday)
    
    return render(request, "enrichmentmanager/assign_all.html", templateData)

@permission_required("enrichmentmanager.can_view_all_advisees")
def all_explicit(request, year, month, day):
    year, month, day = map(int, (year, month, day))
    monday = getMonday(date(year, month, day))
    sunday = monday + timedelta(days=6)
    
    templateData = getTemplateData(request, advisor=None, unassigned=False, monday=monday)
    templateData['allowSlotSort'] = True
    
    #This is horrible ineffecient, but it does solve the quick reassignment issue...
    if request.GET.get("sort"):
        def getKey(student):
            option = EnrichmentOption.objects.filter(slot__id=request.GET['sort'], students=student).first()
            
            if option:
                return (option.teacher.last_name, option.teacher.first_name)
            
            return ("", "")
        
        templateData['students'] = sorted(templateData['students'], key=getKey)
        
    
    return render(request, "enrichmentmanager/assign_all.html", templateData)
