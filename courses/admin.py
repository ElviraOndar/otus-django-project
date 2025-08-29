from django.contrib import admin
from .models import Course, Enrollment
from schedule.models import Lesson

# Register your models here.


class EnrollmentInline(admin.TabularInline):
    model = Enrollment
    extra = 1  # сколько пустых строк показывается в админ-панели для добавления новых студентов
    readonly_fields = ('date_joined',)  # не редактировать дату присоединения


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'short_description', 'teacher', 'get_students')
    list_filter = ('title', 'teacher')

    search_fields = ('title', 'teacher__username')
    inlines = [EnrollmentInline, LessonInline]

    def get_students(self, obj):
        return ", ".join([student.username for student in obj.students.all()])

    get_students.short_description = "Students"


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'date_joined')
    list_filter = ('student', 'course', 'date_joined')

    search_fields = ("student__username", "course__title")






