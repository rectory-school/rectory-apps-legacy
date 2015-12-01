from django.contrib import admin
from django.core import urlresolvers

from adminsortable.admin import SortableAdmin, NonSortableParentAdmin, SortableStackedInline

from courseevaluations.models import QuestionSet, FreeFormQuestion, MultipleChoiceQuestion, MultipleChoiceQuestionOption, EvaluationSet, DormParentEvaluation, CourseEvaluation, IIPEvaluation

class MultipleChoiceQuestionOptionInline(SortableStackedInline):
    model = MultipleChoiceQuestionOption
    
    def get_extra(self, request, obj=None, **kwargs):
        extra = 5
        
        if obj:
            return extra - obj.multiplechoicequestionoption_set.count()
        
        return extra
    
class MultipleChoiceQuestionInline(SortableStackedInline):
    model = MultipleChoiceQuestion
    
    fields = ['question', 'edit_link']
    readonly_fields = ['question', 'edit_link']
    extra = 0
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def edit_link(self, o):
        if o.id:
            return "<a href=\"{0:}\" target=_blank>Edit Question</a>".format(urlresolvers.reverse('admin:courseevaluations_multiplechoicequestion_change', args=(o.id,)))

        return ""
    
    edit_link.allow_tags = True
    edit_link.short_description = 'Edit Link'
        
class MultipleChoiceQuestionAdmin(SortableAdmin):
    inlines = [MultipleChoiceQuestionOptionInline]

class QuestionSetAdmin(NonSortableParentAdmin):
    inlines = [MultipleChoiceQuestionInline]
    
# Register your models here.
admin.site.register(QuestionSet, QuestionSetAdmin)
admin.site.register(FreeFormQuestion, SortableAdmin)
admin.site.register(MultipleChoiceQuestion, MultipleChoiceQuestionAdmin)
admin.site.register(EvaluationSet)
admin.site.register(DormParentEvaluation)
admin.site.register(CourseEvaluation)
admin.site.register(IIPEvaluation)
