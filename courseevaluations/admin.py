from django.contrib import admin
from django.core import urlresolvers
from django.contrib.admin.util import flatten_fieldsets

from adminsortable.admin import SortableAdmin, NonSortableParentAdmin, SortableStackedInline

from courseevaluations.models import QuestionSet, FreeformQuestion, MultipleChoiceQuestion, MultipleChoiceQuestionOption, EvaluationSet, DormParentEvaluation, CourseEvaluation, IIPEvaluation

class ReadOnlyAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if self.declared_fieldsets:
            return flatten_fieldsets(self.declared_fieldsets)
        else:
            return list(set(
                [field.name for field in self.opts.local_fields] +
                [field.name for field in self.opts.local_many_to_many]
            ))
    
    def has_add_permission(self, *args, **kwargs):
        return False
    
    

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

class CourseEvaluationAdmin(ReadOnlyAdmin):
    list_filter = ['evaluation_set__name', ('student', admin.RelatedOnlyFieldListFilter)]

class IIPEvaluationAdmin(ReadOnlyAdmin):
    list_filter = ['evaluation_set__name', ('student', admin.RelatedOnlyFieldListFilter)]
    
class DormParentEvaluationAdmin(ReadOnlyAdmin):
    list_filter = ['evaluation_set__name', 'dorm', ('student', admin.RelatedOnlyFieldListFilter)]
    
# Register your models here.
admin.site.register(QuestionSet, QuestionSetAdmin)
admin.site.register(FreeformQuestion, SortableAdmin)
admin.site.register(MultipleChoiceQuestion, MultipleChoiceQuestionAdmin)
admin.site.register(EvaluationSet)
admin.site.register(CourseEvaluation, CourseEvaluationAdmin)
admin.site.register(IIPEvaluation, IIPEvaluationAdmin)
admin.site.register(DormParentEvaluation, DormParentEvaluationAdmin)
