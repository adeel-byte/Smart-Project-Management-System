from rest_framework.permissions import BasePermission, SAFE_METHODS
from accounts.models import User


def is_admin(user):
    return (
        user.is_authenticated
        and (user.is_superuser or user.role == User.Role.ADMIN)
    )


class ProjectPermission(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:
            return (
                is_admin(request.user)
                or obj.manager_id == request.user.id
                or obj.members.filter(id=request.user.id).exists()
            )

        return (
            is_admin(request.user)
            or obj.manager_id == request.user.id
        )


class MilestonePermission(BasePermission):

    def has_permission(self, request, view):

        if not request.user.is_authenticated:
            return False

        if request.method in SAFE_METHODS:
            return True

        return (
                is_admin(request.user)
                or request.user.role == User.Role.PROJECT_MANAGER
        )

    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:
            return (
                is_admin(request.user)
                or obj.project.manager_id == request.user.id
                or obj.project.members.filter(
                    id=request.user.id
                ).exists()
            )

        return (
            is_admin(request.user)
            or obj.project.manager_id == request.user.id
        )