from django.db import models
from django.conf import settings

# Create your models here.


class Lesson(models.Model):
    class Meta:
        ordering = ['start_time']
        verbose_name = "Занятие"
        verbose_name_plural = "Занятия"

    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, related_name='lessons')

    title = models.CharField(max_length=100)

    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        limit_choices_to={'is_teacher': True},
        null=True,
        blank=True,
        related_name='lessons',
    )

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return f"{self.title} ({self.start_time:%d.%m %H:%M})"


