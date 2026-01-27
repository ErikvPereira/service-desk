from django.urls import path
from .views import tickets_home

urlpatterns = [
    path('tickets/', tickets_home, name='tickets_home'),
]