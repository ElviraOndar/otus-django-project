from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Register your models here.


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email', 'first_name', 'last_name', "is_teacher", "is_student", "is_staff")
    list_filter = ("is_teacher", "is_student", "is_staff", "is_active")

    search_fields = ('username', 'email', 'first_name', 'last_name')

    fieldsets = UserAdmin.fieldsets + (
        ("Роли", {"fields": ("is_teacher", "is_student")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Роли", {"fields": ("is_teacher", "is_student")}),
    )





