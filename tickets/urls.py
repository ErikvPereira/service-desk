from django.urls import path
from .views import tickets_home, login_view, logout_view, ticket_list, ticket_new, ticket_detail

urlpatterns = [
    path('tickets/', ticket_list, name='ticket_list'),
    path('tickets/new/', ticket_new, name='ticket_new'),
    path('tickets/<int:ticket_id>/', ticket_detail, name='ticket_detail'),

    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]