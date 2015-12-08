from django import forms

class SurveyForm(forms.Form):
    def __init__(self, question_set, *args, **kwargs):
        super(SurveyForm, self).__init__(*args, **kwargs)
        
        multiple_choice_questions = question_set.multiplechoicequestion_set.prefetch_related('multiplechoicequestionoption_set').all()
        freeform_questions = question_set.freeformquestion_set.all()
        
        for q in multiple_choice_questions:
            choices = [(opt.id, opt.option) for opt in q.multiplechoicequestionoption_set.all()]
            
            field = forms.ChoiceField(widget=forms.RadioSelect, choices=choices, label=q.question, required=q.required)
            
            self.fields["multiplechoice_{id:}".format(id=q.id)] = field
        
        for q in freeform_questions:
            field = forms.CharField(label=q.question, widget=forms.Textarea, required=q.required)
            
            self.fields["freeform_{id:}".format(id=q.id)] = field