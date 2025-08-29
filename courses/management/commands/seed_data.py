from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from courses.models import Course, Enrollment
from schedule.models import Lesson
from django.utils import timezone
from datetime import timedelta

User = get_user_model()


class Command(BaseCommand):
    help = "Загружает тестовые данные (2 учителя, 6 студентов, 2 курса и уроки)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--flush",
            action="store_true",
            help="Удалить все тестовые данные (учителя, студентов, курсы, уроки, записи).",
        )

    def handle(self, *args, **options):
        if options["flush"]:
            self._flush_data()
            self.stdout.write(self.style.WARNING("🗑 Тестовые данные удалены."))
            return

        # --- Учителя ---
        teacher1, created = User.objects.get_or_create(
            username="teacher1",
            defaults={
                "email": "teacher1@example.com",
                "is_teacher": True,
                "first_name": "Alice",
                "last_name": "Johnson",
            }
        )
        if created:
            teacher1.set_password("password123")
            teacher1.save()

        teacher2, created = User.objects.get_or_create(
            username="teacher2",
            defaults={
                "email": "teacher2@example.com",
                "is_teacher": True,
                "first_name": "Bob",
                "last_name": "Smith",
            }
        )
        if created:
            teacher2.set_password("password123")
            teacher2.save()

        # --- Студенты ---
        students = []
        student_names = [
            ("student1", "John", "Doe"),
            ("student2", "Jane", "Doe"),
            ("student3", "Michael", "Brown"),
            ("student4", "Emily", "Davis"),
            ("student5", "Daniel", "Wilson"),
            ("student6", "Sophia", "Taylor"),
        ]

        for username, first_name, last_name in student_names:
            student, created = User.objects.get_or_create(
                username=username,
                defaults={
                    "email": f"{username}@example.com",
                    "is_teacher": False,
                    "first_name": first_name,
                    "last_name": last_name,
                }
            )
            if created:
                student.set_password("password123")
                student.save()
            students.append(student)

        # --- Курсы ---
        course1, _ = Course.objects.get_or_create(
            title="Python Basics",
            defaults={"description": "Курс для начинающих, которые только делают первые шаги в программировании. Вы освоите основы синтаксиса Python, научитесь работать с переменными, условиями, циклами, функциями и коллекциями. Практические задания помогут закрепить теорию и сразу увидеть результат. По окончании курса вы сможете писать простые программы и будете готовы к дальнейшему изучению Python и разработки приложений.", "teacher": teacher1}
        )
        course2, _ = Course.objects.get_or_create(
            title="Django Web Development",
            defaults={"description": "Практический курс по созданию веб-приложений на Django. Вы научитесь работать с моделями и ORM, проектировать базы данных, создавать формы и админку, а также писать свои API. Разберём маршрутизацию, шаблоны, авторизацию и работу с пользователями. Итогом курса станет готовый проект — полноценное веб-приложение на Django, которое можно развернуть на сервере.", "teacher": teacher2}
        )

        # --- Уроки ---
        Lesson.objects.get_or_create(
            course=course1,
            title="Введение в Python",
            teacher=teacher1,
            start_time=timezone.now().replace(hour=10, minute=0, second=0, microsecond=0) + timedelta(days=1),
            end_time=timezone.now().replace(hour=12, minute=0, second=0, microsecond=0) + timedelta(days=1),
        )
        Lesson.objects.get_or_create(
            course=course1,
            title="Типы данных в Python",
            teacher=teacher1,
            start_time=timezone.now().replace(hour=10, minute=0, second=0, microsecond=0) + timedelta(days=2),
            end_time=timezone.now().replace(hour=12, minute=0, second=0, microsecond=0) + timedelta(days=2),
        )

        Lesson.objects.get_or_create(
            course=course2,
            title="Введение в Django",
            teacher=teacher2,
            start_time=timezone.now().replace(hour=18, minute=0, second=0, microsecond=0) + timedelta(days=3),
            end_time=timezone.now().replace(hour=20, minute=0, second=0, microsecond=0) + timedelta(days=3),
        )
        Lesson.objects.get_or_create(
            course=course2,
            title="Модели и ORM в Django",
            teacher=teacher2,
            start_time=timezone.now().replace(hour=18, minute=0, second=0, microsecond=0) + timedelta(days=4),
            end_time=timezone.now().replace(hour=20, minute=0, second=0, microsecond=0) + timedelta(days=4),
        )

        # --- Записываем студентов на курсы ---
        for student in students:
            Enrollment.objects.get_or_create(student=student, course=course1)
            Enrollment.objects.get_or_create(student=student, course=course2)

        self.stdout.write(self.style.SUCCESS("✅ Seed data успешно загружены!"))

    def _flush_data(self):
        """Удаляем только тестовые данные, чтобы не трогать реальные."""
        Enrollment.objects.filter(student__username__startswith="student").delete()
        Lesson.objects.filter(course__title__in=["Python Basics", "Django Web Development"]).delete()
        Course.objects.filter(title__in=["Python Basics", "Django Web Development"]).delete()
        User.objects.filter(username__in=["teacher1", "teacher2"]).delete()
        User.objects.filter(username__startswith="student").delete()