from rest_framework import serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

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

    @action(detail=True, methods=["post"], url_path="toggle-status")
    def toggle_status(self, request, pk=None):
        ticket = self.get_object()

        if ticket.status == Ticket.Status.CLOSED:
            ticket.status == Ticket.Status.OPEN
        else:
            ticket.status = Ticket.status.CLOSED
            ticket.save(update_fields=[status])
            return Response(
                {"id": ticket.id, "status": ticket.status},
                status=status.HTTP_200_OK,
            )

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
