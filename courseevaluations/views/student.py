from datetime import date

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse

from django.db import transaction

from academics.models import Student
from courseevaluations.models import EvaluationSet, Evaluable, MultipleChoiceQuestion, MultipleChoiceQuestionOption, MultipleChoiceQuestionAnswer, FreeformQuestionAnswer, FreeformQuestion

from courseevaluations.forms import SurveyForm

# Create your views here.
def student_landing(request):
    student = Student.objects.get(auth_key=request.GET["auth_key"])
    
    evaluation_sets = EvaluationSet.objects.filter(available_until__gte=date.today())
    
    evaluables = Evaluable.objects.filter(evaluation_set__in=evaluation_sets, complete=False, student=student).order_by('id')
    completed_evaluations = Evaluable.objects.filter(evaluation_set__in=evaluation_sets, complete=True, student=student).order_by('id')
    
    return render(request, "courseevaluations/student_landing.html", {'evaluables': evaluables, 'student': student, 'completed_evaluations': completed_evaluations})

def student_survey(request):
    student = Student.objects.get(auth_key=request.GET["auth_key"])
    evaluable = Evaluable.objects.get(student=student, pk=request.GET["evaluable"])
    
    landing_url = "{url:}?auth_key={auth_key:}".format(url=reverse('courseevaluations_student_landing'), auth_key=student.auth_key)
    
    if evaluable.complete:
        return redirect(landing_url)
    
    question_set = evaluable.question_set
    
    if request.method == 'POST':
        form = SurveyForm(question_set, request.POST)
        
        if form.is_valid():
            with transaction.atomic():
                MultipleChoiceQuestionAnswer.objects.filter(evaluable=evaluable).delete()
                FreeformQuestionAnswer.objects.filter(evaluable=evaluable).delete()
                
                for key in form.cleaned_data:
                    question_type, id = key.split("_")
                    
                    if not form.cleaned_data[key]:
                        continue
                    
                    if question_type == 'multiplechoice':
                        question = MultipleChoiceQuestion.objects.get(pk=id)
                        selected_option = MultipleChoiceQuestionOption.objects.get(pk=form.cleaned_data[key])
                        
                        assert selected_option.question == question
                        
                        answer = MultipleChoiceQuestionAnswer()
                        answer.evaluable = evaluable
                        answer.answer = selected_option
                        
                        answer.save()
                    
                    elif question_type == 'freeform':
                        question = FreeformQuestion.objects.get(pk=id)
                        answer = FreeformQuestionAnswer()
                        answer.evaluable = evaluable
                        answer.question = question
                        answer.answer = form.cleaned_data[key]
                        
                        answer.save()

                evaluable.complete = True
                evaluable.save()
                return redirect(landing_url)
    else:
        form = SurveyForm(question_set)
        
    return render(request, "courseevaluations/student_survey.html", {'evaluable': evaluable, 'form': form})