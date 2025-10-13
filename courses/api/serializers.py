from rest_framework import serializers
from courses.models import Course, Enrollment
from schedule.models import Lesson
from django.contrib.auth import get_user_model

User = get_user_model()


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')


class LessonSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer(read_only=True)

    class Meta:
        model = Lesson
        fields = ["id", "title", "teacher", "start_time", "end_time"]


class CourseSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer(read_only=True)
    lessons = LessonSerializer(many=True, read_only=True)
    num_students = serializers.IntegerField(read_only=True)

    class Meta:
        model = Course
        fields = ["id", "title", "description", "teacher", "num_students", "lessons"]


class EnrollmentSerializer(serializers.ModelSerializer):
    student = serializers.StringRelatedField(read_only=True)
    course = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Enrollment
        fields = ["id", "student", "course", "date_joined"]



