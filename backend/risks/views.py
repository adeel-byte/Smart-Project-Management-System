
from django.db.models import Q
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied

from accounts.models import User
from .models import Risk
from .serializers import RiskSerializer
from .permissions import RiskPermission, is_admin


class RiskViewSet(viewsets.ModelViewSet):
    serializer_class = RiskSerializer
    permission_classes = [RiskPermission]

    def get_queryset(self):
        user = self.request.user

        if is_admin(user):
            return Risk.objects.all()

        return Risk.objects.filter(
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
                "Only Administrators and Project Managers can create risks."
            )

        project = serializer.validated_data['project']

        if not is_admin(user) and project.manager_id != user.id:
            raise PermissionDenied(
                "You can only create risks in your own projects."
            )

        serializer.save(identified_by=user)
