from datetime import date, timedelta

from django.contrib import admin
from django.contrib.admin.util import flatten_fieldsets
from django.http import HttpResponse

from academics.models import Dorm, AcademicYear, Student, Teacher, Enrollment, Course, Section, StudentRegistration

from academics.lib.student_info_sheet import write_info_sheets

class ReadOnlyAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if self.declared_fieldsets:
            return flatten_fieldsets(self.declared_fieldsets)
        else:
            return list(set(
                [field.name for field in self.opts.local_fields] +
                [field.name for field in self.opts.local_many_to_many]
            ))

class AcademicYearAdmin(admin.ModelAdmin):
    fields = ['year', 'current']
    list_display = ['year', 'current']
    readonly_fields = ['year']

class EnrolledWithinListFilter(admin.SimpleListFilter):
    title = 'enrolled within'
    parameter_name = 'enrolled_within'
    
    def lookups(self, request, model_admin):
        return (
            ('7', '7 days'),
            ('30', '30 days'),
            ('60', '60 days'),
            ('90', '90 days'),
            ('120', '120 days'),
        )
    
    def queryset(self, request, queryset):
        if self.value():
            after_date = date.today() - timedelta(days=int(self.value()))
            
            return queryset.filter(enrollment__enrolled_date__gte=after_date)
            

class StudentAdmin(ReadOnlyAdmin):
    list_display = ['student_id', 'first_name', 'last_name', 'email', 'current']
    list_filter = ['current', EnrolledWithinListFilter]
    
    def get_info_sheet(modeladmin, request, queryset):
        academic_year = AcademicYear.objects.current()
        enrollments = Enrollment.objects.filter(student__in=queryset, academic_year=academic_year)
        
        enrollments = enrollments.order_by('grade', 'student__last_name', 'student__first_name')
        
        response = HttpResponse(content_type='application/pdf')
        
        write_info_sheets(response, enrollments)
        
        return response
    
    actions = ['get_info_sheet']

class TeacherAdmin(ReadOnlyAdmin):
    list_display = ['teacher_id', 'first_name', 'last_name', 'email', 'active']
    list_filter = ['active']

class DormAdmin(admin.ModelAdmin):
    filter_horizontal = ['heads']

class EnrollmentAdmin(ReadOnlyAdmin):
    list_display = ['student', 'academic_year']
    list_filter = ['academic_year__current']

class CourseAdmin(ReadOnlyAdmin):
    list_display = ['number', 'course_name']

class SectionAdmin(ReadOnlyAdmin):
    list_display = ['csn', 'course', 'academic_year', 'teacher']
    list_filter = ['academic_year']

class StudentRegistrationAdmin(ReadOnlyAdmin):
    list_filter = ['section__academic_year']
    list_display = ['student_reg_id', 'section', 'student']
    
# Register your models here.
admin.site.register(Dorm, DormAdmin)
admin.site.register(AcademicYear, AcademicYearAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Enrollment, EnrollmentAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(StudentRegistration, StudentRegistrationAdmin)