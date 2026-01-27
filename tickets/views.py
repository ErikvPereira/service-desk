from django.shortcuts import render

# Create your views here.
def tickets_home(request):
    return render(request, 'tickets/home.html')
