from enrichmentmanager.models import EnrichmentSignup, EnrichmentOption

from enrichmentmanager.lib import canEditSignup

from io import StringIO
from datetime import date

from django import template
register = template.Library()

@register.assignment_tag(takes_context=True)
def select_for(context, slot, student):
    
    if student.lockout:
        return '<p class="readOnlySignup">{lockout}</p>'.format(lockout=student.lockout)
    
    canEdit = canEditSignup(context.request.user, slot, student)
    
    key = "slot_{slot_id}_{student_id}".format(slot_id=slot.id, student_id=student.id)
    
    if canEdit:
        out = StringIO()
        choices = context['slotChoices'][slot]

        out.write('<select name="{key}_option" class="slotSelector saveTrack">'.format(key=key))
        out.write('<option value="">--</option>')
    
        selected = context['relatedSignups'].get(key)
        
        preferredChoices = StringIO()
        otherChoices = StringIO()
        associatedTeachers = student.associated_teachers.all()
        
        for choice in choices:
            if choice.teacher in associatedTeachers:
                if selected == choice.id:
                    preferredChoices.write('<option value="{choice_id}" selected="selected">{choice_name}</option>'.format(choice_id=choice.id, choice_name=str(choice)))
                else:
                    preferredChoices.write('<option value="{choice_id}">{choice_name}</option>'.format(choice_id=choice.id, choice_name=str(choice)))
            else:
                if selected == choice.id:
                    otherChoices.write('<option value="{choice_id}" selected="selected">{choice_name}</option>'.format(choice_id=choice.id, choice_name=str(choice)))
                else:
                    otherChoices.write('<option value="{choice_id}">{choice_name}</option>'.format(choice_id=choice.id, choice_name=str(choice)))
        
        preferredChoices = preferredChoices.getvalue()
        otherChoices = otherChoices.getvalue()
        
        if preferredChoices and otherChoices:
            out.write(preferredChoices)
            out.write('<option value="">--</option>')
            out.write(otherChoices)
        
        else:
            out.write(preferredChoices)
            out.write(otherChoices)
                
        out.write("</select>")
        
        if context.request.user.has_perm("enrichmentmanager.can_set_admin_lock"):
            #TODO: Horribly ineffecient
            try:
                signup = EnrichmentSignup.objects.get(slot=slot, student=student)
            except EnrichmentSignup.DoesNotExist:
                signup = None
            
            if signup and signup.admin_lock:
                out.write('<input type="checkbox" title="Admin Lockout" name="{key}_adminlock" class="saveTrack adminLock" checked />'.format(key=key))
            else:
                out.write('<input type="checkbox" title="Admin Lockout" name="{key}_adminlock" class="saveTrack adminLock" />'.format(key=key))
        
        return out.getvalue()
    
    else:
        selectedID = context['relatedSignups'].get(key)
        
        if selectedID:
            #Ineffecient, will generate many queries if viewing in read only mode
            selectedChoice = EnrichmentOption.objects.get(pk=selectedID)

            return '<p class="readOnlySignup">{option}</p>'.format(option=selectedChoice)
        
        return ""
    
@register.assignment_tag(takes_context=True)
def display_for(context, slot, student):
    if student.lockout:
        return "<em title='Lockout assigned'>{}</em>".format(student.lockout)
        
    key = "slot_{slot_id}_{student_id}".format(slot_id=slot.id, student_id=student.id)
    
    selected = context['relatedSignups'].get(key, "")
    
    if selected:
        return str(EnrichmentOption.objects.get(pk=selected))
    
    return "<strong>Unassigned</strong>"
    