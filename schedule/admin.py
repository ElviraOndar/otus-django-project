from django.contrib import admin
from .models import Lesson

# Register your models here.


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "teacher", "start_time", "end_time")
    list_filter = ("course", "teacher", "start_time")
    search_fields = ("title", "description", "course__title")
