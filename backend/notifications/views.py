from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Notification
from .serializers import NotificationSerializer


class NotificationViewSet(viewsets.ModelViewSet):

    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Users can only access their own notifications
        return Notification.objects.filter(
            recipient=self.request.user
        )

    def perform_create(self, serializer):
        # Automatically assign notification to logged-in user
        serializer.save(recipient=self.request.user)