from rest_framework.permissions import BasePermission
from .models import User


class IsAdministrator(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (
                request.user.is_superuser
                or request.user.role == User.Role.ADMIN
            )
        )


class IsProjectManagerOrAdministrator(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (
                request.user.is_superuser
                or request.user.role in [
                    User.Role.ADMIN,
                    User.Role.PROJECT_MANAGER
                ]
            )
        )