from courseevaluations.models import StudentEmailTemplate
from academics.models import Student

def send_student_email_from_template(template_id, student_id, override_email=None):
    student = Student.objects.get(pk=student_id)
    template = StudentEmailTemplate.objects.get(pk=template_id)
    
    msg = template.get_message(student)
    
    if override_email:
        msg.to = [override_email]
    
    msg.send()
    