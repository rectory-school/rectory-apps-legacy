from django.contrib import admin
from django.core import urlresolvers
from django.contrib.admin.util import flatten_fieldsets

from adminsortable.admin import SortableAdmin, NonSortableParentAdmin, SortableStackedInline

from courseevaluations.models import QuestionSet, FreeformQuestion, MultipleChoiceQuestion, MultipleChoiceQuestionOption, EvaluationSet, DormParentEvaluation, CourseEvaluation, IIPEvaluation, MultipleChoiceQuestionAnswer, FreeformQuestionAnswer, StudentEmailTemplate
from academics.models import Student

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

class CourseEvaluationAdmin(admin.ModelAdmin):
    search_fields = ['student__first_name', 'student__last_name', 'student__email']
    list_display = ['__str__', 'complete']
    
    class EvaluationSetListFilter(admin.SimpleListFilter):
        title = 'evaluation set'
        parameter_name = 'evaluation_set_id'
    
        def lookups(self, request, model_admin):
            return [(es.id, es.name) for es in EvaluationSet.objects.all()]
        
        def queryset(self, request, queryset):
            if self.value():
                return queryset.filter(evaluation_set__id=self.value())
            
            return queryset
    
    class StudentListFilter(admin.SimpleListFilter):
        title = 'student'
        parameter_name = 'student_id'
        
        def lookups(self, request, model_admin):
            current_evaluables = model_admin.get_queryset(request)
            students = Student.objects.filter(evaluable__in=current_evaluables).distinct()
        
            return [(student.id, student.name) for student in students]
        
        def queryset(self, request, queryset):
            if self.value():
                return queryset.filter(student__id=self.value())
                
            return queryset
    
    list_filter = [EvaluationSetListFilter, 'complete', StudentListFilter]

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
admin.site.register(StudentEmailTemplate)