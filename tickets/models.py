from django.conf import settings
from django.db import models

# Create your models here.


class Ticket(models.Model):
    class Category(models.TextChoices):
        BUG = "BUG", "Bug"
        ACCESS = "ACCESS", "Acesso"
        QUESTION = "QUESTION", "Dúvida"
        OTHER = "OTHER", "Outro"

    class Priority(models.TextChoices):
        LOW = "LOW", "Baixa"
        MEDIUM = "MEDIUM", "Média"
        HIGH = "HIGH", "Alta"
        URGENT = "URGENT", "Urgente"

    class Status(models.TextChoices):
        OPEN = "OPEN", "Aberto"
        IN_PROGRESS = "IN_PROGRESS", "Em andamento"
        RESOLVED = "RESOLVED", "Resolvido"
        CLOSED = "CLOSED", "Fechado"

    title = models.CharField(max_length=120)
    description = models.TextField()
    category = models.CharField(
        max_length=20, 
        choices=Category.choices,
        default=Category.OTHER)
    priority = models.CharField(
        max_length=20, 
        choices=Priority.choices, 
        default=Priority.MEDIUM)
    status = models.CharField(
        max_length=20, 
        choices=Status.choices, 
        default=Status.OPEN)

    requester = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="tickets"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"#{self.id} {self.title}"

class TicketComment(models.Model):
    ticket = models.ForeignKey("Ticket", on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment on #{self.ticket_id}"
