import email.utils

from django.template.loader import get_template
from django.template import Context
from django.core.mail import EmailMessage

from detention_notifier.models import Detention, DetentionMailer, DetentionCC
from academics.models import AcademicYear, Enrollment

def get_body(detention):
    term_detentions = Detention.objects.filter(
                                        student=detention.student,
                                        term=detention.term,
                                        offense__mail=True
                                        ).order_by('detention date')
        
    detention_mailer = DetentionMailer.objects.get()
    
    if detention.offense:
        offense = detention.offense
    elif detention_mailer.blank_offense:
        offense = detention_mailer.blank_offense
    else:
        raise ValueError("Cannot get offense for internal detention {}".format(detention.id))
    
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
        'term_detentions': term_detentions,
        'detention_mailer': detention_mailer
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

def get_message(detention):
    subject = get_subject(detention)
    body = get_body(detention)
    detention_mailer = DetentionMailer.objects.get()
    
    student = detention.student
    
    academic_year = AcademicYear.objects.current()
    
    #May throw an exception, which is what we want if we can't get an enrollment - let it fly up
    enrollment = Enrollment.objects.get(student=student, academic_year=detention.term.academic_year)
    
    advisor = enrollment.advisor
    tutor = enrollment.tutor
    
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
        email = additional_address.address
        mail_type = additional_address.mail_type
        
        #message.to, message.cc, message.bcc
        mail_list = getattr(message, mail_type)
        
        if email not in mail_list:
            mail_list.append(email)

    if detention_mailer.advisor_mail and advisor:
        #message.to, message.cc, etc
        mail_list = getattr(detention_mailer.advisor_mail, message)
        email = advisor.email
        
        if not email in mail_list:
            mail_list.append(email)
    
    if detention_mailer.tutor_mail and tutor:
        mail_list = getattr(detention_mailer.tutor_mail, message)
        email = tutor.email
        
        if not email in mail_list:
            mail_list.append(email)
    
    if detention_mailer.reply_to_from:
        #This was set above
        message.reply_to.append(message.from_email)
    
    if detention_mailer.reply_to_advisor and advisor and advisor.email:
        advisor_addr = email.utils.formataddr((advisor.name, advisor.email))
        message.reply_to.append(advisor_addr)
    
    if detention_mailer.reply_to_tutor and tutor and tutor.email:
        tutor_addr = email.utils.formataddr((tutor.name, tutor.email))
        message.reply_to.append(tutor_addr)
    
    
    return message