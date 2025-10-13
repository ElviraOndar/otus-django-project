from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsTeacherOrReadOnly(BasePermission):
    """Преподаватели могут создавать, редактировать и удалять курсы.
    Студенты и анонимные пользователи могут только читать.
    Суперюзер имеет все права."""
    def has_permission(self, request, view):
        # Все безопасные методы (GET, HEAD, OPTIONS) доступны всем
        if request.method in SAFE_METHODS:
            return True
        # Суперюзер может всё
        if request.user.is_authenticated and request.user.is_superuser:
            return True
        # Остальное — только преподаватель
        return bool(request.user and request.user.is_authenticated and request.user.is_teacher)


class IsStudent(BasePermission):
    """
    Только студенты могут записываться на курс.
    Суперюзер может записываться независимо от флага is_student.
    """
    def has_permission(self, request, view):
        # суперюзер может всё
        if request.user.is_authenticated and request.user.is_superuser:
            return True
        return request.user.is_authenticated and request.user.is_student

