from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import TicketForm
from .models import Ticket

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
            return redirect("ticket_list")
        messages.error(request, 'Usuário ou senha inválidos.')
    return render(request, 'auth/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def ticket_list(request):
    tickets = Ticket.objects.filter(requester=request.user).order_by('-created_at')
    return render(request, 'tickets/list.html', {'tickets': tickets})

@login_required
def ticket_new(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.requester = request.user
            ticket.save()
            return redirect('ticket_list')
    else:
        form = TicketForm()
    return render(request, 'tickets/new.html', {'form': form})

@login_required
def ticket_detail(request, ticket_id: int):
    ticket = get_object_or_404(Ticket, id=ticket_id, requester=request.user)
    return render(request, 'tickets/detail.html', {'ticket': ticket})