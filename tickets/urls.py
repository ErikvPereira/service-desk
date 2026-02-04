from django.urls import path

from .views import login_view, logout_view, ticket_detail, ticket_list, ticket_new, toggle_ticket_status

urlpatterns = [
    path("tickets/", ticket_list, name="ticket_list"),
    path("tickets/new/", ticket_new, name="ticket_new"),
    path("tickets/<int:ticket_id>/", ticket_detail, name="ticket_detail"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("tickets/<int:ticket_id>/toggle-status/", toggle_ticket_status, name="toggle_ticket_status"),

]
