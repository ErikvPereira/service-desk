from rest_framework import serializers, viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Ticket


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = [
            "id",
            "title",
            "description",
            "category",
            "priority",
            "status",
            "created_at",
        ]
        read_only_fields = ["id", "created_at", "status"]


class TicketViewSet(viewsets.ModelViewSet):
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Ticket.objects.filter(requester=self.request.user).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(requester=self.request.user)
