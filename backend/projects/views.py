from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from django.db.models import Q

from accounts.models import User
from .models import Project, Milestone
from .serializers import ProjectSerializer, MilestoneSerializer
from .permissions import (
    ProjectPermission,
    MilestonePermission,
    is_admin,
)


class ProjectViewSet(viewsets.ModelViewSet):

    serializer_class = ProjectSerializer
    permission_classes = [ProjectPermission]

    def get_queryset(self):
        user = self.request.user

        if is_admin(user):
            return Project.objects.all()

        return Project.objects.filter(
            Q(manager=user) | Q(members=user)
        ).distinct()

    def perform_create(self, serializer):
        user = self.request.user

        if not (
            is_admin(user)
            or user.role == User.Role.PROJECT_MANAGER
        ):
            raise PermissionDenied(
                "Only Administrators and Project Managers can create projects."
            )

        serializer.save(manager=user)


class MilestoneViewSet(viewsets.ModelViewSet):

    serializer_class = MilestoneSerializer
    permission_classes = [MilestonePermission]

    def get_queryset(self):
        user = self.request.user

        if is_admin(user):
            return Milestone.objects.all()

        return Milestone.objects.filter(
            Q(project__manager=user) |
            Q(project__members=user)
        ).distinct()

    def perform_create(self, serializer):
        user = self.request.user
        project = serializer.validated_data['project']

        if not (
            is_admin(user)
            or project.manager_id == user.id
        ):
            raise PermissionDenied(
                "Only the project manager or administrator can create milestones."
            )

        serializer.save()