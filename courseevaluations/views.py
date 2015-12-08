from datetime import date

from django.shortcuts import render

from academics.models import Student
from courseevaluations.models import EvaluationSet, Evaluable

# Create your views here.
def student_landing(request):
    student = Student.objects.get(auth_key=request.GET["auth_key"])
    
    evaluation_sets = EvaluationSet.objects.filter(available_until__gte=date.today())
    
    evaluables = Evaluable.objects.filter(evaluation_set__in=evaluation_sets, complete=False, student=student).order_by('id')
        
    return render(request, "courseevaluations/student_landing.html", {'evaluables': evaluables, 'student': student})