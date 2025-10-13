from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, CourseEnrollView

router = DefaultRouter()

# DRF Router для CourseViewSet
router.register(r'courses', CourseViewSet, basename='course')

# Дополнительные кастомные эндпоинты, которые не входят в ViewSet
urlpatterns = [
    path('courses/<int:pk>/enroll/', CourseEnrollView.as_view(), name='course-enroll'),
]

# Объединяем с маршрутами из Router
urlpatterns += router.urls




