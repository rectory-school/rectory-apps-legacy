import email
import email.utils

from django.template.loader import get_template
from django.template import Context
from django.core.mail import EmailMessage, send_mail

from detention_notifier.models import Detention, DetentionMailer, DetentionCC, DetentionTo
from academics.models import AcademicYear, Enrollment, StudentParentRelation

def get_body(detention):
    term_detentions = Detention.objects.filter(
                                        student=detention.student,
                                        term=detention.term,
                                        offense__mail=True
                                        ).order_by('detention_date')
        
    detention_mailer = DetentionMailer.objects.get()
    
    if detention.offense:
        offense = detention.offense
    elif detention_mailer.blank_offense:
        offense = detention_mailer.blank_offense
    else:
        raise ValueError("Cannot get offense for internal detention {}. Blank offense is not defined.".format(detention.id))
    
    out_term_detentions = []
    
    for term_detention in term_detentions:
        if term_detention.offense:
            out_term_detentions.append((term_detention, term_detention.offense))
        elif detention_mailer.blank_offense:
            out_term_detentions.append((term_detention, detention_mailer.blank_offense))
        else:
            raise ValueError("Cannot get offense for internal detention {}".format(detention.id))
    
    context = {
        'student': detention.student,
        'teacher': detention.teacher,
        'detention': detention,
        'term_detentions': out_term_detentions,
        'term_detention_count': len(out_term_detentions),
        'detention_mailer': detention_mailer,
        'offense': offense,
    }
    
    template = get_template('detention_notifier/detention_email.txt')
        
    context = Context(context)
    
    return template.render(context)

def get_subject(detention):
    context = {
        'student': detention.student,
    }
    
    context = Context(context)
    
    template = get_template('detention_notifier/detention_subject.txt')
    
    return template.render(context)

def get_message(detention, override_recipients=[]):
    subject = get_subject(detention)
    body = get_body(detention)
    detention_mailer = DetentionMailer.objects.get()
    
    student = detention.student
    
    academic_year = AcademicYear.objects.current()
    
    #May throw an exception, which is what we want if we can't get an enrollment - let it fly up
    enrollment = Enrollment.objects.get(student=student, academic_year=detention.term.academic_year)
    
    advisor = enrollment.advisor
    tutor = enrollment.tutor
    assigner = detention.teacher
    
    message = EmailMessage()
    
    message.subject = subject
    message.body = body
    
    from_name = detention_mailer.from_name
    from_email = detention_mailer.from_email
    
    message.from_email = email.utils.formataddr((from_name, from_email))
    message.to = []
    message.cc = []
    message.bcc = []
    message.reply_to = []
    
    detention_to_objects = DetentionTo.objects.filter(mailer=detention_mailer)
    
    for detention_to_object in detention_to_objects:
        family_id_key = detention_to_object.family_id_key
        parent_code = detention_to_object.parent_code
        
        try:
            relation = StudentParentRelation.objects.get(student=detention.student,
                                                         family_id_key=family_id_key,
                                                         parent_code=parent_code)
                                                        
            if relation.parent.email and relation.parent.email not in message.to:
                message.to.append(relation.parent.email)
                
        except StudentParentRelation.DoesNotExist:
            pass
    
    for additional_address in DetentionCC.objects.filter(mailer=detention_mailer):
        address = additional_address.address
        mail_type = additional_address.mail_type
        
        #message.to, message.cc, message.bcc
        mail_list = getattr(message, mail_type)
        
        if address not in mail_list:
            mail_list.append(address)

    if detention_mailer.advisor_mail and advisor:
        #message.to, message.cc, etc
        mail_list = getattr(message, detention_mailer.advisor_mail)
        address = advisor.email
        
        if not address in mail_list:
            mail_list.append(address)
    
    if detention_mailer.tutor_mail and tutor:
        mail_list = getattr(message, detention_mailer.tutor_mail)
        address = tutor.email
        
        if not address in mail_list:
            mail_list.append(address)
    
    if detention_mailer.assigner_mail and assigner:
        mail_list = getattr(message, detention_mailer.assigner_mail)
        address = assigner.email
    
        if not address in mail_list:
            mail_list.append(address)
        
    
    if detention_mailer.reply_to_from:
        #This was set above
        message.reply_to.append(message.from_email)
    
    if detention_mailer.reply_to_advisor and advisor and advisor.email:
        advisor_addr = email.utils.formataddr((advisor.name, advisor.email))
        
        if not advisor_addr in message.reply_to:
            message.reply_to.append(advisor_addr)
    
    if detention_mailer.reply_to_tutor and tutor and tutor.email:
        tutor_addr = email.utils.formataddr((tutor.name, tutor.email))
        
        if not tutor_addr in message.reply_to:
            message.reply_to.append(tutor_addr)
    
    if detention_mailer.reply_to_assigner and assigner and assigner.email:
        assigner_addr = email.utils.formataddr((assigner.name, assigner.email))
        
        if not assigner_addr in message.reply_to:
            message.reply_to.append(assigner_addr)
    
    #Fix up the recipients - make sure someone isn't in multiple recipient lists. 
    #We've already checked when adding that one person isn't in a recipient list twice.
    for to_person in message.to:
        #Remove from both cc and bcc
        for mail_list in [message.cc, message.bcc]:
            while to_person in mail_list:
                mail_list.remove(to_person)
    
    
    for cc_person in message.cc:
        #Remove CC from BCC
        while cc_person in message.bcc:
            message.bcc.remove(cc_person)
    
    #BCC can cascade down and does not need any special processing.
    
    if override_recipients:
        ammendment_context = Context({
            'to_addresses': message.to,
            'cc_addresses': message.cc,
            'bcc_addressses': message.bcc
        })
        ammendment_body = get_template('detention_notifier/sample_ammendment.txt').render(ammendment_context)
        
        message.body = message.body + ammendment_body
        
        message.to = override_recipients
        message.cc = []
        message.bcc = []
    
    return message