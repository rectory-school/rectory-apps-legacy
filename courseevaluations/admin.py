from django.contrib import admin, messages
from django.urls import reverse
from django.contrib.admin.utils import flatten_fieldsets
from django.http import HttpResponse
from django.conf.urls import url
from django.shortcuts import redirect, get_object_or_404
from django.db import transaction
from django.contrib.auth.decorators import permission_required

from adminsortable.admin import SortableAdmin, NonSortableParentAdmin, SortableStackedInline

from courseevaluations.models import QuestionSet, FreeformQuestion, MultipleChoiceQuestion, MultipleChoiceQuestionOption, EvaluationSet, DormParentEvaluation, CourseEvaluation, IIPEvaluation, MultipleChoiceQuestionAnswer, FreeformQuestionAnswer, StudentEmailTemplate, MELPEvaluation
from academics.models import Student, AcademicYear, Enrollment, Section, Course, Teacher

from academics.utils import fmpxmlparser

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

class FreeformQuestionInline(SortableStackedInline):
    model = FreeformQuestion
    
    fields = ['question', 'edit_link']
    readonly_fields = ['question', 'edit_link']
    extra = 0
    
    def has_add_permission(self, request):
        return False
        
    def has_delete_permission(self, request, obj=None):
        return False
    
    def edit_link(self, o):
        if o.id:
            return "<a href=\"{0:}\" target=_blank>Edit Question</a>".format(reverse('admin:courseevaluations_freeformquestion_change', args=(o.id,)))
    
    edit_link.allow_tags = True
    edit_link.short_description = 'Edit Link'
    
    
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
            return "<a href=\"{0:}\" target=_blank>Edit Question</a>".format(reverse('admin:courseevaluations_multiplechoicequestion_change', args=(o.id,)))

        return ""
    
    edit_link.allow_tags = True
    edit_link.short_description = 'Edit Link'
        
class MultipleChoiceQuestionAdmin(SortableAdmin):
    inlines = [MultipleChoiceQuestionOptionInline]

class QuestionSetAdmin(NonSortableParentAdmin):
    inlines = [MultipleChoiceQuestionInline, FreeformQuestionInline]

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

class EvaluationSetAdmin(admin.ModelAdmin):
    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        
        extra_context["question_sets"] = QuestionSet.objects.all()
        
        return super().change_view(request=request, object_id=object_id, form_url=form_url, extra_context=extra_context)
    
    def create_iip_evaluations(self, request, object_id):
        redirect_url = reverse('admin:courseevaluations_evaluationset_change', args=(object_id, ))
        
        if not request.user.has_perm('courseevaluations.add_iipevaluation'):
            messages.error(request, "You do not have the appropriate permissions to add IIP evaluations")
            return redirect(redirect_url)
        
        if request.method != 'POST':
            messages.error(request, "Invalid request, please try again. No evaluations created.")
            return redirect(redirect_url)
        
        question_set_id = request.POST.get("question_set_id")
        
        if not question_set_id:
            messages.error(request, "Question set is required. No evaluations created.")
            return redirect(redirect_url)
        
        iip_evaluation_file = request.FILES.get('iip_evaluation_file')
        
        if not iip_evaluation_file:
            messages.error(request, "IIP evaluation file is required. No evaluations created.")
            return redirect(redirect_url)
            
        data = fmpxmlparser.parse_from_file(iip_evaluation_file)
        results = data['results']
        
        creation_count = 0
        
        with transaction.atomic():
            question_set = get_object_or_404(QuestionSet, pk=question_set_id)
            evaluation_set = get_object_or_404(EvaluationSet, pk=object_id)
            academic_year = AcademicYear.objects.current()
            
            for row in results:
                fields = row['parsed_fields']
                
                student_id = fields['IDStudent']
                teacher_id = fields['SectionTeacher::IDTEACHER']
                
                student = Student.objects.get(student_id=student_id)
                teacher = Teacher.objects.get(teacher_id=teacher_id)
                enrollment = Enrollment.objects.get(student=student, academic_year=academic_year)
                
                evaluable = IIPEvaluation()
                evaluable.student = student
                evaluable.teacher = teacher
                evaluable.evaluation_set = evaluation_set
                evaluable.question_set = question_set
                evaluable.enrollment = enrollment
                
                evaluable.save()
                
                creation_count += 1
        
        messages.add_message(request, messages.SUCCESS, "Successfully created {count:} IIP evaluations".format(count=creation_count))
        return redirect(redirect_url)
        
    def create_course_evaluations(self, request, object_id):
        redirect_url = reverse('admin:courseevaluations_evaluationset_change', args=(object_id, ))
        
        if not request.user.has_perm('courseevaluations.add_courseevaluation'):
            messages.error(request, "You do not have the appropriate permissions to add course evaluations")
            return redirect(redirect_url)
        
        if request.method != 'POST':
            messages.error(request, "Invalid request, please try again. No evaluations created.")
            return redirect(redirect_url)
        
        course_type = request.POST.get("course_type")
        
        #Course class will be the either a MELPEvaluation or a CourseEvaluation
        if course_type == "melp":
            CourseClass = MELPEvaluation
        elif course_type == "course":
            CourseClass = CourseEvaluation
        else:
            messages.error(request, "Course type is not defined. No evaluations created.")
            return redirect(redirect_url)
        
        question_set_id = request.POST.get("question_set_id")
        
        if not question_set_id:
            messages.error(request, "Question set is required. No evaluations created.")
            return redirect(redirect_url)
        
        course_evaluation_file = request.FILES.get('course_evaluation_file')
        
        if not course_evaluation_file:
            messages.error(request, "Course evaluation file is required. No evaluations created.")
            return redirect(redirect_url)
            
        data = fmpxmlparser.parse_from_file(course_evaluation_file)
        results = data['results']
        
        creation_count = 0
        
        with transaction.atomic():
            question_set = get_object_or_404(QuestionSet, pk=question_set_id)
            evaluation_set = get_object_or_404(EvaluationSet, pk=object_id)
            
            for row in results:
                fields = row['parsed_fields']
                
                csn = fields['CourseSectionNumber']
                academic_year = fields['AcademicYear']
                
                section = Section.objects.get(csn=csn, academic_year__year=academic_year)
                
                for student in section.students.all():
                    enrollment = Enrollment.objects.get(student=student, academic_year__year=academic_year)
                    
                    evaluable = CourseClass()
                    evaluable.student = student
                    evaluable.enrollment = enrollment
                    evaluable.section = section
                    evaluable.question_set = question_set
                    evaluable.evaluation_set = evaluation_set
                    evaluable.save()
                    
                    creation_count += 1
        
        messages.add_message(request, messages.SUCCESS, "Successfully created {count:} course evaluations".format(count=creation_count))
        return redirect(redirect_url)
    
    def create_dorm_parent_evaluations(self, request, object_id):
        redirect_url = reverse('admin:courseevaluations_evaluationset_change', args=(object_id, ))
        
        if not request.user.has_perm('courseevaluations.add_dormparentevaluation'):
            messages.error(request, "You do not have the appropriate permissions to add IIP evaluations")
            return redirect(redirect_url)
        
        if request.method != 'POST':
            messages.error(request, "Invalid request, please try again. No evaluations created.")
            return redirect(redirect_url)
        
        question_set_id = request.POST.get("question_set_id")
        
        if not question_set_id:
            messages.error(request, "Question set is required. No evaluations created.")
            return redirect(redirect_url)
        
        with transaction.atomic():
            question_set = get_object_or_404(QuestionSet, pk=question_set_id)
            evaluation_set = get_object_or_404(EvaluationSet, pk=object_id)
            
            academic_year = AcademicYear.objects.current()
            
            enrollments = Enrollment.objects.filter(student__current=True, academic_year=academic_year).exclude(dorm=None)
            
            creation_count = 0
            
            for enrollment in enrollments:
                student = enrollment.student
                dorm = enrollment.dorm
                heads = dorm.heads.all()
                
                for teacher in heads:
                    evaluable = DormParentEvaluation()
                    evaluable.question_set = question_set
                    evaluable.evaluation_set = evaluation_set
                    
                    evaluable.dorm = dorm
                    evaluable.parent = teacher
                    evaluable.student = student
                    evaluable.enrollment = enrollment
                    
                    evaluable.save()
                    creation_count += 1
        
        messages.add_message(request, messages.SUCCESS, "Successfully created {count:} dorm parent evaluations".format(count=creation_count))
        
        return redirect(redirect_url)
    
    def get_urls(self):
        urls = super().get_urls()
        
        my_urls = [
            url(r'^(?P<object_id>[0-9]+)/process/create/dorm/parent/$', 
                self.admin_site.admin_view(self.create_dorm_parent_evaluations),
                name='courseevaluations_evaluationset_create_dorm_parent_evals'),

            url(r'^(?P<object_id>[0-9]+)/process/create/course/$', 
                self.admin_site.admin_view(self.create_course_evaluations),
                name='courseevaluations_evaluationset_create_course_evals'),
                
            url(r'^(?P<object_id>[0-9]+)/process/create/iip/$', 
                self.admin_site.admin_view(self.create_iip_evaluations),
                name='courseevaluations_evaluationset_create_iip_evals'),
        ]
        
        return my_urls + urls

class MELPEvaluationAdmin(CourseEvaluationAdmin):
    pass
    
class IIPEvaluationAdmin(ReadOnlyAdmin):
    list_filter = ['evaluation_set__name', ('student', admin.RelatedOnlyFieldListFilter)]
    
class DormParentEvaluationAdmin(ReadOnlyAdmin):
    list_filter = ['evaluation_set__name', 'dorm', ('student', admin.RelatedOnlyFieldListFilter)]
    
# Register your models here.
admin.site.register(QuestionSet, QuestionSetAdmin)
admin.site.register(FreeformQuestion, SortableAdmin)
admin.site.register(MultipleChoiceQuestion, MultipleChoiceQuestionAdmin)
admin.site.register(EvaluationSet, EvaluationSetAdmin)
admin.site.register(CourseEvaluation, CourseEvaluationAdmin)
admin.site.register(MELPEvaluation, MELPEvaluationAdmin)
admin.site.register(IIPEvaluation, IIPEvaluationAdmin)
admin.site.register(DormParentEvaluation, DormParentEvaluationAdmin)
admin.site.register(StudentEmailTemplate)