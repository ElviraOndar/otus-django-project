from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Course, Enrollment

# Create your views here.


class CoursesListView(ListView):
    model = Course
    template_name = 'courses/courses_list.html'
    context_object_name = 'courses'


class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/course_detail.html'
    context_object_name = 'course'
