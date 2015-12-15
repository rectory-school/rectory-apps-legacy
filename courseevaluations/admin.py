from django.contrib import admin
from django.core import urlresolvers
from django.contrib.admin.util import flatten_fieldsets

from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin

from adminsortable.admin import SortableAdmin, NonSortableParentAdmin, SortableStackedInline

from courseevaluations.models import QuestionSet, FreeformQuestion, MultipleChoiceQuestion, MultipleChoiceQuestionOption, EvaluationSet, DormParentEvaluation, CourseEvaluation, IIPEvaluation, MultipleChoiceQuestionAnswer, FreeformQuestionAnswer, StudentEmailTemplate, Evaluable, DormEvaluation
from academics.models import Student

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

class FreeformQuestionInline(SortableStackedInline):
    model = FreeformQuestion
    
    fields = ['question', 'edit_link']
    readonly_fields = ['question', 'edit_link']
    
    def has_add_permission(self, request):
        return False
        
    def has_delete_permission(self, request, obj=None):
        return False
        
    def edit_link(self, o):
        if o.id:
            return "<a href=\"{0:}\" target=_blank>Edit Question</a>".format(urlresolvers.reverse('admin:courseevaluations_freeformquestion_change', args=(o.id,)))

        return ""
    
    edit_link.allow_tags = True
    edit_link.short_description = 'Edit Link'

class MultipleChoiceQuestionAdmin(SortableAdmin):
    inlines = [MultipleChoiceQuestionOptionInline]

class QuestionSetAdmin(NonSortableParentAdmin):
    inlines = [MultipleChoiceQuestionInline, FreeformQuestionInline]

class EvaluableChildAdmin(PolymorphicChildModelAdmin):
    base_model = Evaluable
    
    base_fieldsets = (
        ('Basic Information', {'fields': ('student', 'evaluation_set', 'question_set', 'complete')}),
    )

class CourseEvaluationAdmin(EvaluableChildAdmin):
    base_model = CourseEvaluation

class IIPEvaluationAdmin(EvaluableChildAdmin):
    base_model = IIPEvaluation

class DormEvaluationAdmin(EvaluableChildAdmin):
    base_model = DormEvaluation
    
class DormParentEvaluationAdmin(DormEvaluationAdmin):
    base_model = DormParentEvaluation
    
class EvaluableParentAdmin(PolymorphicParentModelAdmin):
    base_model = Evaluable
    
    polymorphic_list = True
    
    list_filter = ['student']
    list_display = ['student_display', 'student', 'evaluation_type_title', '__str__']
    
    
    child_models = (
        (CourseEvaluation, CourseEvaluationAdmin),
        (IIPEvaluation, IIPEvaluationAdmin),
        (DormEvaluation, DormEvaluationAdmin),
        (DormParentEvaluation, DormParentEvaluationAdmin),
    )
    
# Register your models here.
admin.site.register(QuestionSet, QuestionSetAdmin)
admin.site.register(FreeformQuestion, SortableAdmin)
admin.site.register(MultipleChoiceQuestion, MultipleChoiceQuestionAdmin)
admin.site.register(EvaluationSet)
admin.site.register(StudentEmailTemplate)
admin.site.register(Evaluable, EvaluableParentAdmin)