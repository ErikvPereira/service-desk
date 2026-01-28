from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def tickets_home(request):
    return render(request, 'tickets/home.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('tickets_home')
        messages.error(request, 'Usuário ou senha inválidos.')
    return render(request, 'auth/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')
