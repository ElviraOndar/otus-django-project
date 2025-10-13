"""
URL configuration for CodeCourse project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    # HTML Views
    path('admin/', admin.site.urls),
    path('', include('courses.urls')),  # HTML routes
    path('contacts/', include('contacts.urls')),

    # REST API
    path('api/', include('courses.api.urls')),  # DRF API routes
    path('api-auth/', include('rest_framework.urls')),  # для тестирования в браузере
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),   # получение access и refresh токена
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # обновление access токена
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

