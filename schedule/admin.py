from django.contrib import admin
from .models import Lesson
from django import forms
from django.contrib.admin.widgets import AdminSplitDateTime


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1


class LessonAdminForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = "__all__"
        widgets = {
            "start_time": AdminSplitDateTime(),
            "end_time": AdminSplitDateTime(),
        }


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    form = LessonAdminForm
    list_display = ("title", "course", "teacher", "start_time", "end_time")
    list_filter = ("course", "teacher", "start_time")
    search_fields = ("title", "course__title")





