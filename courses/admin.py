from django.contrib import admin
from .models import Course, Enrollment

# Register your models here.


class EnrollmentInline(admin.TabularInline):
    model = Enrollment
    extra = 1  # сколько пустых строк показывается в админ-панели для добавления новых студентов


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'short_description', 'teacher')
    list_filter = ('teacher',)

    search_fields = ('title', 'description', 'teacher')
    inlines = [EnrollmentInline]


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'date_joined')
    list_filter = ('student', 'course', 'date_joined')

    search_fields = ("student__username", "course__title")






