from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def tickets_home(request):
    return HttpResponse('Tickets app funcionando')