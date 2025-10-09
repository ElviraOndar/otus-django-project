import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CodeCourse.settings")

app = Celery("CodeCourse")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()


