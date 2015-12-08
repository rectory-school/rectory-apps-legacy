from django.contrib import admin
from django.contrib.admin.util import flatten_fieldsets

from academics.models import Dorm, AcademicYear, Student, Teacher, Enrollment, Course, Section, StudentRegistration

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

class StudentAdmin(ReadOnlyAdmin):
    list_display = ['student_id', 'first_name', 'last_name', 'email', 'current']
    list_filter = ['current']

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