from django.db.models import Q
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied

from accounts.models import User
from .models import Task
from .serializers import TaskSerializer
from .permissions import TaskPermission, is_admin


class TaskViewSet(viewsets.ModelViewSet):

    serializer_class = TaskSerializer
    permission_classes = [TaskPermission]

    def get_queryset(self):
        user = self.request.user

        if is_admin(user):
            return Task.objects.all()

        return Task.objects.filter(
            Q(project__manager=user) |
            Q(project__members=user)
        ).distinct()

    def perform_create(self, serializer):
        user = self.request.user

        if not (
            is_admin(user)
            or user.role == User.Role.PROJECT_MANAGER
        ):
            raise PermissionDenied(
                "Only Administrators and Project Managers can create tasks."
            )

        project = serializer.validated_data['project']

        if not is_admin(user) and project.manager_id != user.id:
            raise PermissionDenied(
                "You can only create tasks in your own projects."
            )

        serializer.save(created_by=user)

    def update(self, request, *args, **kwargs):
        task = self.get_object()

        if (
            not is_admin(request.user)
            and task.project.manager_id != request.user.id
        ):
            if request.method != 'PATCH':
                raise PermissionDenied(
                    "Team Members can only update task status."
                )

            if set(request.data.keys()) != {'status'}:
                raise PermissionDenied(
                    "Team Members can only change the status of their assigned tasks."
                )

        return super().update(request, *args, **kwargs)