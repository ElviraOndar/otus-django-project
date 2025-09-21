from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Course
from .forms import CourseForm
from django.urls import reverse_lazy
from django.db.models import Count, Prefetch
from schedule.models import Lesson

# Create your views here.


class CoursesListView(ListView):
    model = Course
    template_name = 'courses/courses_list.html'
    context_object_name = 'courses'

    def get_queryset(self):
        """Подгружаем преподавателя одним JOIN и считаем студентов одной SQL-командой"""
        return Course.objects.select_related('teacher').annotate(num_students=Count('students'))


class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/course_detail.html'
    context_object_name = 'course'

    def get_queryset(self):
        # Создаём Prefetch для уроков с преподавателем
        lessons_prefetch = Prefetch(
            'lessons',
            queryset=Lesson.objects.select_related('teacher').order_by('start_time')
        )
        return Course.objects.select_related('teacher').prefetch_related(
            'students',
            lessons_prefetch
        )


class CourseCreateView(CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'courses/course_form.html'
    success_url = reverse_lazy('courses:courses')


class CourseUpdateView(UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'courses/course_form.html'
    success_url = reverse_lazy('courses:courses')


class CourseDeleteView(DeleteView):
    model = Course
    template_name = 'courses/course_confirm_delete.html'
    success_url = reverse_lazy('courses:courses')




