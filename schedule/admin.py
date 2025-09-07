from django.contrib import admin
from .models import Lesson
from .forms import LessonAdminForm


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    form = LessonAdminForm
    list_display = ("title", "course", "teacher", "start_time", "end_time")
    list_filter = ("course", "teacher", "start_time")
    search_fields = ("title", "course__title")





