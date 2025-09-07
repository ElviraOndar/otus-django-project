from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Course
from .forms import CourseForm
from django.urls import reverse_lazy

# Create your views here.


class CoursesListView(ListView):
    model = Course
    template_name = 'courses/courses_list.html'
    context_object_name = 'courses'


class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/course_detail.html'
    context_object_name = 'course'


class CourseCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'courses/course_form.html'
    success_url = reverse_lazy('courses:courses')

    def test_func(self):
        # Только преподаватели или админы могут создавать курс
        return self.request.user.is_teacher or self.request.user.is_staff


class CourseUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'courses/course_form.html'
    success_url = reverse_lazy('courses:courses')

    def test_func(self):
        # Только преподаватели или админы могут обновлять курс
        return self.request.user.is_teacher or self.request.user.is_staff


class CourseDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Course
    template_name = 'courses/course_confirm_delete.html'
    success_url = reverse_lazy('courses:courses')

    def test_func(self):
        # Только преподаватели или админы могут удалять курс
        return self.request.user.is_teacher or self.request.user.is_staff

