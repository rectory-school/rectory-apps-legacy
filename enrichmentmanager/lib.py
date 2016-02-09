#!/usr/bin/python

from datetime import datetime, date, timedelta

from enrichmentmanager.models import EnrichmentSlot, Teacher, Student, EnrichmentSignup, EnrichmentOption
from django.contrib.auth.models import Permission

from django.utils import timezone

import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

def getMonday(d):
    return d - timedelta(days=d.weekday())

def getUnassignedStudents(slots):
    missingStudents = set()
    
    for slot in slots:
        signups = EnrichmentSignup.objects.filter(slot=slot)
        missingStudents |= set(Student.objects.exclude(enrichmentsignup__in=signups))
    
    lockouts = Student.objects.exclude(lockout="")
    missingStudents -= set(lockouts)
    
    return missingStudents

def getUnassignedAdvisors(slots):
    students = getUnassignedStudents(slots)
    
    advisors = {}
    
    for student in students:
        advisor = student.advisor
        if advisor not in advisors:
            advisors[advisor] = set()
        
        advisors[advisor].add(student)
    
    return advisors

def getRoomCounts(forWeek):
    monday = getMonday(forWeek)
    sunday = monday + timedelta(days=6)

    slots = EnrichmentSlot.objects.filter(date__gte=monday).filter(date__lte=sunday).order_by('date')

    out = {}

    for slot in slots:
        out[slot] = {}
    
        for option in slot.enrichmentoption_set.all():
            studentCount = option.students.count()
            location = option.location
        
            if not location in out[slot]:
                out[slot][location] = {'count': 0, 'options': []}
        
            out[slot][location]['count'] += studentCount
            
            out[slot][location]['options'].append({'option': option, 'count': studentCount})
    
    return out

def canEditSignup(user, slot, student):
    if not user:
        logger.warn("Attempted save without being logged in")
        return False
    
    if slot.date < date.today():
        logger.warn("Attempted save of a slot in the past")
        return False
    
    if not user.has_perm("enrichmentmanager.can_edit_same_day") and slot.editable_until:
        if timezone.now() > slot.editable_until:
            logger.warn("Attempted save of same day without permission")
            return False
    
    try:
        signup = EnrichmentSignup.objects.get(student=student, slot=slot)
        
        if signup.admin_lock and not user.has_perm("enrichmentmanager.can_override_admin_lock"):
            return False
            
    except EnrichmentSignup.DoesNotExist:
        pass
    
    if student.lockout:
        logger.warn("Attempted save of locked out student")
        return False
    
    if user.has_perm("enrichmentmanager.can_edit_all_advisees"):
        return True
    
    if user.has_perm("enrichmentmanager.can_edit_own_advisees"):
        if student.advisor.email == request.user.email:
            return True
    
    
    
    logger.warn("Attempted save fallthrough failure")
    return False