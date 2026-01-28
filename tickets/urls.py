from django.urls import path
from .views import tickets_home, login_view, logout_view

urlpatterns = [
    path('tickets/', tickets_home, name='tickets_home'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout')
]