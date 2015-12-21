#!/usr/bin/python

from copy import copy, deepcopy
from collections import deque

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch

from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, PageBreak, Flowable
from reportlab.platypus.doctemplate import ActionFlowable

styles = getSampleStyleSheet()

base_style = styles["Normal"]
base_style.fontName = "Helvetica"

title_style = copy(base_style)
name_style = copy(base_style)
header_style = copy(base_style)
subheader_style = copy(base_style)
normal_style = copy(base_style)

#Text: 23, 54, 93
#Line: 79, 129, 189
title_style.textColor = colors.Color(23/256, 54/256, 93/256)
title_style.fontSize = 20
title_style.leading = 24

name_style.textColor = colors.grey
name_style.fontSize = 14
name_style.leading = 16

#Text: 52, 90, 138
header_style.textColor = colors.Color(52/256, 90/256, 138/256)
header_style.fontSize = 18
header_style.leading = 22
header_style.spaceBefore = 18

subheader_style.fontName = 'Helvetica-Bold'


#Pops an element off the enrollments attribute to advance the student
#one more in the enrollments attr
class NextStudent(ActionFlowable):
    def apply(self, doc):
        if doc.enrollments:
            doc.current_enrollment = doc.enrollments.popleft()
        else:
            doc.current_enrollment = None

def story_for_info_sheet(enrollment):
    username = enrollment.student.username
    password = enrollment.student.rectory_password
    name = enrollment.student.last_name_first
    grade = enrollment.grade
    email = enrollment.student.email
    
    elementary = grade in ('k', '1', '2', '3', '4')
    
    story = []
    
    story.append(Paragraph("Rectory School Student Info Sheet", title_style))
    story.append(Paragraph(name, name_style))
    
    if username and password:
        story.append(Paragraph("Logging onto Rectory Computers", header_style))
        story.append(Paragraph("To log into a Rectory computer (Rooms 313/314, library, etc):", subheader_style))
        story.append(Paragraph("Turn the computer on, if it is not already on", normal_style, bulletText='-'))
        story.append(Paragraph("Enter your username: {username:}".format(username=username), normal_style, bulletText='-'))
        story.append(Paragraph("Enter your password: {password:}".format(password=password), normal_style, bulletText='-'))
        story.append(Paragraph("Press return to log into the computer", normal_style, bulletText='-'))
    
    if email and password:
        story.append(Paragraph("Logging onto a Chromebook", header_style))
        story.append(Paragraph("To log into a Rectory computer (Rooms 313/314, library, etc):", subheader_style))
        story.append(Paragraph("Turn the Chromebook on, if it is not already on", normal_style, bulletText='-'))
        story.append(Paragraph("Enter your email: {username:}".format(username=email), normal_style, bulletText='-'))
        story.append(Paragraph("Press enter", normal_style, bulletText='-'))
        story.append(Paragraph("Enter your password: {password:}".format(password=password), normal_style, bulletText='-'))
        story.append(Paragraph("Press enter to log onto the computer", normal_style, bulletText='-'))
        
    if email and password and not elementary:
        story.append(Paragraph("E-mail", header_style))
        story.append(Paragraph("To access your @rectorywolves.org e-mail:", subheader_style))
        story.append(Paragraph("Using a web browser (Chrome, Safari, Firefox), navigate to gmail.com", normal_style, bulletText='-'))
        story.append(Paragraph("Enter your Rectory e-mail address: {email:}".format(email=email), normal_style, bulletText='-'))
        story.append(Paragraph("Enter your password: {password:}".format(password=password), normal_style, bulletText='-'))
    
    story.append(Paragraph("Printing", header_style))
    story.append(Paragraph("All Rectory printers have been installed on student computers that have been seen by the Technology office. If you have a computer on campus and need to print, please stop by the Technology Office to have printers installed.", normal_style))
    
    if username and password and not elementary:
        story.append(Paragraph("Wireless Access", header_style))
        story.append(Paragraph('After the first week of school, the <i>rectory-student-open</i> network will be removed. You can connect to the Rectory network using the following credentials:', normal_style))
        story.append(Paragraph("Username: {username:}".format(username=username), normal_style, bulletText='-'))
        story.append(Paragraph("Password: {password:}".format(password=password), normal_style, bulletText='-'))
    
    if email and password and not elementary:
        story.append(Paragraph("Schoology", header_style))
        story.append(Paragraph("To access Schoology at www.schoology.com:", subheader_style))
        story.append(Paragraph("Username: {username:}".format(username=email), normal_style, bulletText='-'))
        story.append(Paragraph("Password: {password:}".format(password=password), normal_style, bulletText='-'))
    
    return story

def write_info_sheets(output, enrollments):
    story = []
    
    enrollment_queue = deque()
    
    for enrollment in enrollments:
        enrollment_queue.append(enrollment)
        story.extend(story_for_info_sheet(enrollment))
        story.append(NextStudent())
        story.append(PageBreak())
        
    
    #Makes the assumption of one page per student sheet
    def draw_footer(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 12)
        
        canvas.setStrokeColor(colors.grey)
        canvas.setFillColor(colors.grey)
        
        enrollment = doc.current_enrollment
        if enrollment:
            canvas.drawString(.75*inch, .75*inch, enrollment.student.last_name_first)
            canvas.drawRightString(7.75*inch, .75*inch, "Grade: {}".format(enrollment.grade))
        
        canvas.restoreState()
    
    doc = SimpleDocTemplate(output, pagesize=(8.5*inch, 11*inch))
    doc.enrollments = enrollment_queue
    #Pop the first enrollment so current_enrollment is accurate and NextStudent() works property
    doc.current_enrollment = doc.enrollments.popleft()
    doc.build(story, onFirstPage=draw_footer, onLaterPages=draw_footer)
    