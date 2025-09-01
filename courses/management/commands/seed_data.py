from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from courses.models import Course, Enrollment
from schedule.models import Lesson
from django.utils import timezone
from datetime import timedelta

User = get_user_model()


class Command(BaseCommand):
    help = "Загружает тестовые данные (группы, 2 учителя, 6 студентов, 2 курса, уроки и записи)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--flush",
            action="store_true",
            help="Удалить все тестовые данные (группы, пользователей, курсы, уроки, записи)",
        )

    def handle(self, *args, **options):
        if options["flush"]:
            self._flush_data()
            self.stdout.write(self.style.WARNING("🗑 Тестовые данные удалены"))
            return

        # Создаем группы
        teachers_group, created_t = Group.objects.get_or_create(name="teachers")
        students_group, created_s = Group.objects.get_or_create(name="students")

        lesson_ct = ContentType.objects.get_for_model(Lesson)
        course_ct = ContentType.objects.get_for_model(Course)

        if created_t:
            teacher_permissions = Permission.objects.filter(
                content_type__in=[lesson_ct, course_ct],
                codename__in=[
                    "add_lesson", "change_lesson", "delete_lesson", "view_lesson",
                    "add_course", "change_course", "delete_course", "view_course",
                ],
            )
            teachers_group.permissions.set(teacher_permissions)
            self.stdout.write(self.style.SUCCESS("👨‍🏫 Группа teachers создана и получила права"))

        if created_s:
            student_permissions = Permission.objects.filter(
                content_type__in=[lesson_ct, course_ct],
                codename__in=["view_lesson", "view_course"],
            )
            students_group.permissions.set(student_permissions)
            self.stdout.write(self.style.SUCCESS("👩‍🎓 Группа students создана и получила права"))

        # Учителя
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
        teacher1.groups.add(teachers_group)

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
        teacher2.groups.add(teachers_group)

        # Студенты
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
                    "is_student": True,
                    "first_name": first_name,
                    "last_name": last_name,
                }
            )
            if created:
                student.set_password("password123")
                student.save()
            student.groups.add(students_group)
            students.append(student)

        # Курсы
        course1, _ = Course.objects.get_or_create(
            title="Python Basics",
            defaults={"description": "Курс для начинающих, которые только делают первые шаги в программировании. Вы освоите основы синтаксиса Python, работу с переменными, условиями, циклами, функциями и коллекциями. Практические задания помогут закрепить теорию и сразу увидеть результат. После курса вы сможете писать простые программы и будете готовы к дальнейшему изучению Python и разработке приложений", "teacher": teacher1}
        )
        course2, _ = Course.objects.get_or_create(
            title="Django Web Development",
            defaults={"description": "Практический курс по созданию веб-приложений на Django. Вы научитесь работать с моделями и ORM, проектировать базы данных, создавать формы и админку, а также писать свои API. Разберем маршрутизацию, шаблоны, авторизацию и работу с пользователями. Итогом курса станет готовый проект — полноценное веб-приложение на Django, которое можно развернуть на сервере", "teacher": teacher2}
        )

        # Записываем студентов на оба курса
        for student in students:
            Enrollment.objects.get_or_create(student=student, course=course1)
            Enrollment.objects.get_or_create(student=student, course=course2)

        # Ставим в расписание уроки по обоим курсам
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

        self.stdout.write(self.style.SUCCESS("✅ Seed data успешно загружены!"))

    def _flush_data(self):
        """Удаляем только тестовые данные, чтобы не трогать реальные"""
        Enrollment.objects.filter(student__username__startswith="student").delete()
        Lesson.objects.filter(course__title__in=["Python Basics", "Django Web Development"]).delete()
        Course.objects.filter(title__in=["Python Basics", "Django Web Development"]).delete()
        User.objects.filter(username__in=["teacher1", "teacher2"]).delete()
        User.objects.filter(username__startswith="student").delete()
        Group.objects.filter(name__in=["teachers", "students"]).delete()