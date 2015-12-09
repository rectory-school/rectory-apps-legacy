from courseevaluations.models import StudentEmailTemplate
from academics.models import Student
from django.core.mail import send_mail

def send_student_email_from_template(template_id, student_id, override_email=None):
    student = Student.objects.get(pk=student_id)
    template = StudentEmailTemplate.objects.get(pk=template_id)
    
    msg = template.get_message(student)
    
    if override_email:
        msg.to = [override_email]
    
    msg.send()

def send_confirmation_email(addresses, to_addresses):
    body = "Your e-mail was sent to the following {count:} people: \n\n{addresses:}".format(count=len(addresses), addresses="\n".join(addresses))
    
    send_mail("Message confirmation", body, "technology@rectoryschool.org", to_addresses)