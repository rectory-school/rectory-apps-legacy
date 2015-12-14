#!/usr/bin/python

from django.views.generic.base import TemplateView
from courseevaluations.models import EvaluationSet

class AdminLanding(TemplateView):
    template_name = "courseevaluations/adminlanding.html"
    
    def get_context_data(self, **kwargs):
        context = super(TemplateView, self).get_context_data(**kwargs)
        evaluation_sets = EvaluationSet.objects.all()
        
        if 'evaluation_set_id' in kwargs:
            evaluation_sets = evaluation_sets.filter(pk=kwargs['evaluation_set_id'])
            
        context['evaluation_sets'] = evaluation_sets
            
        return context