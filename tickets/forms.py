from django import forms
from .models import Ticket, TicketComment

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ["title", "description", "category", "priority"]

class CommentForm(forms.ModelForm):
    class Meta:
        model = TicketComment
        fields = ['message']
        