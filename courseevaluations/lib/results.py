#!/usr/bin/python

from io import BytesIO

from reportlab.lib import enums
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, KeepTogether, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch

from courseevaluations.models import QuestionSet, MultipleChoiceQuestionAnswer, FreeformQuestionAnswer

title_style = ParagraphStyle(getSampleStyleSheet()["Normal"])
question_set_style = ParagraphStyle(getSampleStyleSheet()["Normal"])
question_style = ParagraphStyle(getSampleStyleSheet()["Normal"])
multiple_choice_option_style = ParagraphStyle(getSampleStyleSheet()["Normal"])
multiple_choice_count_style = ParagraphStyle(getSampleStyleSheet()["Normal"])
freeform_answer_style = ParagraphStyle(getSampleStyleSheet()["Normal"])

title_style.fontSize = 20
title_style.leading = 24
title_style.alignment = enums.TA_RIGHT
title_style.fontName = 'Times-BoldItalic'

question_style.spaceBefore = 10
question_style.fontName = 'Times-Bold'
question_style.fontSize = 12

multiple_choice_option_style.alignment = enums.TA_CENTER
multiple_choice_count_style.alignment = enums.TA_CENTER

freeform_answer_style.fontSize = 8

def build_report(output, evaluables, title=None, comments=True, unmask_comments=False):
    doc_args = {
        'author': 'Rectory School Evaluation System',
        'pagesize': letter,
        'leftMargin': 36,
        'rightMargin': 36,
    }
    
    if title:
        doc_args['title'] = title
    
    inner_width = doc_args['pagesize'][0] - doc_args['leftMargin'] - doc_args['rightMargin']
        
    story = []
    
    if title:
        story.append(Paragraph(title, title_style))
    
    question_sets = QuestionSet.objects.filter(evaluable__in=evaluables).distinct()
    
    for question_set in question_sets:
        if question_sets.count() > 1:
            story.append(Paragraph(question_set.name, question_set_style))
            
        for question in question_set.multiplechoicequestion_set.all():
            answer_labels = []
            answer_counts = []
            
            for option in question.multiplechoicequestionoption_set.all():
                count = MultipleChoiceQuestionAnswer.objects.filter(evaluable=evaluables, answer=option).count()
                
                answer_labels.append(Paragraph(option.option, multiple_choice_option_style))
                answer_counts.append(Paragraph(str(count), multiple_choice_count_style))
            
            cols = len(answer_labels)
            t = Table([answer_labels, answer_counts], cols*[inner_width/cols])
            
            together = [
                Paragraph(question.question, question_style),
                t
            ]
            story.append(Spacer(1, 4))
            story.append(KeepTogether(together))
                        
        if comments:
            for question in question_set.freeformquestion_set.all():
                together = []
                together.append(Paragraph(question.question, question_style))
                together.append(Spacer(1, .1*inch))
                
                for answer in FreeformQuestionAnswer.objects.filter(evaluable__in=evaluables, question=question).order_by("?"):
                    if unmask_comments:
                        display_answer = "({student:}) {answer:}".format(student=answer.evaluable.student.name, answer=answer.answer)
                    else:
                        display_answer = answer.answer
                        
                    together.append(Paragraph(display_answer, freeform_answer_style, bulletText='-'))
                
                story.append(KeepTogether(together))
        
    doc = SimpleDocTemplate(output, **doc_args)
    doc.build(story)