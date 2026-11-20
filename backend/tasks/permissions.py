from rest_framework.permissions import BasePermission, SAFE_METHODS
from accounts.models import User


def is_admin(user):
    return (
        user.is_authenticated
        and (
            user.is_superuser
            or user.role == User.Role.ADMIN
        )
    )


class TaskPermission(BasePermission):

    def has_permission(self, request, view):

        if not request.user.is_authenticated:
            return False

        if request.method in SAFE_METHODS:
            return True

        if request.method == 'POST':
            return (
                is_admin(request.user)
                or request.user.role == User.Role.PROJECT_MANAGER
            )

        return True

    def has_object_permission(self, request, view, obj):

        user = request.user

        if request.method in SAFE_METHODS:
            return (
                is_admin(user)
                or obj.project.manager_id == user.id
                or obj.project.members.filter(id=user.id).exists()
            )

        if is_admin(user) or obj.project.manager_id == user.id:
            return True

        # Team members can update the status of their own tasks.
        return (
            request.method == 'PATCH'
            and obj.assigned_to_id == user.id
        )