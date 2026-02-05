from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q
from django.views.decorators.http import require_POST

from .forms import CommentForm, TicketForm
from .models import Ticket


# Create your views here.
def tickets_home(request):
    return render(request, "tickets/home.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("ticket_list")
        messages.error(request, "Usuário ou senha inválidos.")
    return render(request, "auth/login.html")


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def ticket_list(request):
    qs = Ticket.objects.filter(requester=request.user).order_by("-created_at")

    q = request.GET.get("q", "").strip()
    status = request.GET.get("status", "").strip()

    category = request.GET.get("category", "").strip()

    priority = request.GET.get("priority", "").strip()

    if priority:
        qs = qs.filter(priority=priority)


    if category:
        qs = qs.filter(category=category)

    if q:
        qs = qs.filter(Q(title__icontains=q) | Q(description__icontains=q))

    if status:
        qs = qs.filter(status=status)

    return render(
        request,
        "tickets/list.html",
        {
            "tickets": qs,
            "q": q,
            "status": status,
            "category": category,
            'priority': priority,
            "category_choices": Ticket._meta.get_field("category").choices,
            "priority_choices": Ticket._meta.get_field("priority").choices,
        },
    )

@login_required
def ticket_new(request):
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.requester = request.user
            ticket.save()
            return redirect("ticket_list")
    else:
        form = TicketForm()
    return render(request, "tickets/new.html", {"form": form})


@login_required
def ticket_detail(request, ticket_id: int):
    ticket = get_object_or_404(Ticket, id=ticket_id, requester=request.user)

    if request.method == "POST":
        if ticket.status == Ticket.Status.CLOSED:
            messages.error(request, "Ticket fechado não pode receber comentários.")
            return redirect("ticket_detail", ticket_id=ticket.id)

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.ticket = ticket
            comment.author = request.user
            comment.save()
            return redirect("ticket_detail", ticket_id=ticket.id)
    else:
        form = CommentForm()

    comments = ticket.comments.select_related("author").order_by("created_at")
    return render(
        request,
        "tickets/detail.html",
        {"ticket": ticket, "comments": comments, "form": form},
    )

@login_required
@require_POST
def toggle_ticket_status(request, ticket_id: int):
    ticket = get_object_or_404(Ticket, id=ticket_id, requester=request.user)

    if ticket.status == Ticket.Status.CLOSED:
        ticket.status = Ticket.Status.IN_PROGRESS
        messages.success(request, "Ticket reaberto (Em andamento).")
    else:
        ticket.status = Ticket.Status.CLOSED
        messages.success(request, "Ticket fechado.")

    ticket.save(update_fields=["status"])
    return redirect("ticket_detail", ticket_id=ticket.id)
