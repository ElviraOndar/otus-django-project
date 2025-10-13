from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.db.models import Count, Prefetch
from courses.models import Course, Enrollment
from schedule.models import Lesson
from .serializers import CourseSerializer, EnrollmentSerializer
from .permissions import IsTeacherOrReadOnly, IsStudent


class CourseViewSet(viewsets.ModelViewSet):
    """
    API для курсов (просмотр, создание, редактирование, удаление).
    Студенты могут только читать, а преподаватели могут редактировать
    """
    serializer_class = CourseSerializer
    permission_classes = [IsTeacherOrReadOnly]

    def get_queryset(self):
        lessons_prefetch = Prefetch(
            "lessons",
            queryset=Lesson.objects.select_related("teacher").order_by("start_time"),
        )
        return Course.objects.select_related("teacher").prefetch_related(
            "students", lessons_prefetch
        ).annotate(num_students=Count("students"))

    def perform_create(self, serializer):
        #  Преподаватель автоматически становится учителем курса
        serializer.save(teacher=self.request.user)


class CourseEnrollView(APIView):
    """
    POST /api/courses/<id>/enroll/ — записаться на курс (могут только студенты)
    DELETE /api/courses/<id>/enroll/ — отписаться от курса
    GET /api/courses/<id>/enroll/ — проверить статус
    """
    permission_classes = [IsStudent]

    def post(self, request, pk):
        """записаться на курс"""
        course = get_object_or_404(Course, pk=pk)
        if Enrollment.objects.filter(student=request.user, course=course).exists():
            return Response({"detail": "Вы уже записаны на этот курс."}, status=status.HTTP_400_BAD_REQUEST)

        enrollment = Enrollment.objects.create(student=request.user, course=course)
        serializer = EnrollmentSerializer(enrollment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        """Отписаться от курса"""
        course = get_object_or_404(Course, pk=pk)
        enrollment = Enrollment.objects.filter(student=request.user, course=course).first()
        if not enrollment:
            return Response({"detail": "Вы не записаны на этот курс."}, status=status.HTTP_400_BAD_REQUEST)
        enrollment.delete()
        return Response({"detail": "Вы успешно отписались от курса."}, status=status.HTTP_204_NO_CONTENT)

    def get(self, request, pk):
        """Проверить, записан ли студент на курс"""
        course = get_object_or_404(Course, pk=pk)
        enrolled = Enrollment.objects.filter(student=request.user, course=course).exists()
        return Response({"enrolled": enrolled})

