from django import forms
from django.contrib.admin.widgets import AdminSplitDateTime
from .models import Lesson


class LessonAdminForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = "__all__"
        widgets = {
            "start_time": AdminSplitDateTime(),
            "end_time": AdminSplitDateTime(),
        }


