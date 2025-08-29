from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["username"]

    def __str__(self):
        if self.is_teacher and self.is_student:
            role = "Преподаватель/Студент"
        elif self.is_teacher:
            role = "Преподаватель"
        elif self.is_student:
            role = "Студент"
        else:
            role = "Админ"
        return f"{self.username} ({role})"






