from django.contrib import admin

from courseevaluations.models import QuestionSet, MultipleChoiceQuestion, MultipleChoiceQuestionOption, EvaluationSet, DormParentEvaluation, CourseEvaluation, IIPEvaluation

class MultipleChoiceQuestionOptionInline(admin.TabularInline):
    model = MultipleChoiceQuestionOption

class MultipleChoiceQuestionAdmin(admin.ModelAdmin):
    inlines = [MultipleChoiceQuestionOptionInline]

# Register your models here.
admin.site.register(QuestionSet)
admin.site.register(MulitpleChoiceQuestion, MultipleChoiceQuestionAdmin)
admin.site.register(EvaluationSet)
admin.site.register(DormParentEvaluation)
admin.site.register(CourseEvaluation)
admin.site.register(IIPEvaluation)
