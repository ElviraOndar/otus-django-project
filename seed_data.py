from django.contrib.auth import get_user_model
from courses.models import Course
from schedule.models import Lesson
from django.utils import timezone
from datetime import timedelta

User = get_user_model()


def run():
    # --- Учителя ---
    teacher1, _ = User.objects.get_or_create(
        username="Suren_Khorenyan",
        defaults={"email": "teacher1@example.com", "is_teacher": True}
    )
    teacher2, _ = User.objects.get_or_create(
        username="Aleksandr_Ignatyev",
        defaults={"email": "teacher2@example.com", "is_teacher": True}
    )

    # --- Ученики ---
    for i in range(1, 7):
        User.objects.get_or_create(
            username=f"student{i}",
            defaults={"email": f"student{i}@example.com", "is_teacher": False}
        )

    # --- Курсы ---
    course1, _ = Course.objects.get_or_create(
        title="Python Professional",
        defaults={
            "description":
                "Python Professional — это углублённый курс по программированию на Python, ориентированный на разработчиков, которые уже знакомы с основами языка и хотят вывести свои навыки на профессиональный уровень."}
    )
    course2, _ = Course.objects.get_or_create(
        title="Django Web Development",
        defaults={"description": "Django Advanced — это углублённый курс по одному из самых популярных Python-фреймворков. На занятиях мы разберём внутренние механизмы Django и научимся строить масштабируемые, безопасные и производительные веб-приложения."}
    )

    # --- Уроки ---
    Lesson.objects.get_or_create(
        course=course1,
        title="Введение в Python",
        teacher=teacher1,
        start_time=timezone.now() + timedelta(days=1, hours=10),
        end_time=timezone.now() + timedelta(days=1, hours=12),
    )
    Lesson.objects.get_or_create(
        course=course1,
        title="Типы данных в Python",
        teacher=teacher1,
        start_time=timezone.now() + timedelta(days=2, hours=10),
        end_time=timezone.now() + timedelta(days=2, hours=12),
    )

    Lesson.objects.get_or_create(
        course=course2,
        title="Введение в Django",
        teacher=teacher2,
        start_time=timezone.now() + timedelta(days=3, hours=10),
        end_time=timezone.now() + timedelta(days=3, hours=12),
    )
    Lesson.objects.get_or_create(
        course=course2,
        title="Модели и ORM в Django",
        teacher=teacher2,
        start_time=timezone.now() + timedelta(days=4, hours=10),
        end_time=timezone.now() + timedelta(days=4, hours=12),
    )