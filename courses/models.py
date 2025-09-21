from django.db import models
from django.conf import settings
import textwrap

# Create your models here.


class Course(models.Model):
    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    title = models.CharField(max_length=200, unique=True, null=False, blank=False)
    description = models.TextField()

    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="courses_taught",
        limit_choices_to={"is_teacher": True},
    )

    def get_teacher_name(self):
        return f"{self.teacher.first_name} {self.teacher.last_name}".strip()

    students = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="Enrollment",
        related_name="enrolled_courses",
    )

    def __str__(self):
        return self.title

    def short_description(self):
        return textwrap.shorten(self.description, width=70, placeholder=" <...>")

    short_description.short_description = "Short Description"


class Enrollment(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["student", "course"], name="uniq_student_course"
            )
        ]
        verbose_name = "Запись на курс"
        verbose_name_plural = "Запись на курс"

    student = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                limit_choices_to={'is_student': True},
                                )
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} → {self.course}"







