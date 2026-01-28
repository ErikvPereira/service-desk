from django.urls import path
from .views import tickets_home, login_view, logout_view, ticket_list, ticket_new


urlpatterns = [
    path('tickets/', ticket_list, name='ticket_list'),
    path('tickets/new/', ticket_new, name='ticket_new'),

    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]