import pytest
from django.contrib.auth import get_user_model

from tickets.models import Ticket, TicketComment

pytestmark = pytest.mark.django_db


def create_user(username="erik", password="12345678"):
    User = get_user_model()
    return User.objects.create_user(username=username, password=password)


def test_logged_user_can_create_ticket(client):
    user = create_user()
    client.login(username="erik", password="12345678")

    resp = client.post(
        "/tickets/new/",
        data={
            "title": "Meu primeiro ticket",
            "description": "Descrição do ticket",
            "category": "BUG",
            "priority": "MEDIUM",
        },
        follow=True,
    )

    assert resp.status_code == 200
    assert Ticket.objects.count() == 1
    ticket = Ticket.objects.first()
    assert ticket.requester == user
    assert ticket.title == "Meu primeiro ticket"


def test_logged_user_can_comment_on_own_ticket(client):
    user = create_user()
    client.login(username="erik", password="12345678")

    ticket = Ticket.objects.create(
        title="Ticket com comentário",
        description="Desc",
        category="BUG",
        priority="MEDIUM",
        requester=user,
    )

    resp = client.post(
        f"/tickets/{ticket.id}/",
        data={"message": "Primeiro comentário"},
        follow=True,
    )

    assert resp.status_code == 200
    assert TicketComment.objects.count() == 1
    comment = TicketComment.objects.first()
    assert comment.ticket_id == ticket.id
    assert comment.author == user
    assert comment.message == "Primeiro comentário"


def test_ticket_list_filters_by_query_and_status(client):
    user = create_user()
    client.login(username="erik", password="12345678")

    Ticket.objects.create(
        title="Erro no login",
        description="Falha ao entrar",
        category="BUG",
        priority="MEDIUM",
        status="OPEN",
        requester=user,
    )
    Ticket.objects.create(
        title="Outra coisa",
        description="Nada a ver",
        category="BUG",
        priority="MEDIUM",
        status="CLOSED",
        requester=user,
    )

    resp = client.get("/tickets/?q=login&status=OPEN")
    assert resp.status_code == 200
    content = resp.content.decode()
    assert "Erro no login" in content
    assert "Outra coisa" not in content


def test_user_can_close_and_reopen_own_ticket(client):
    user = create_user()
    client.login(username="erik", password="12345678")

    ticket = Ticket.objects.create(
        title="Fechar ticket",
        description="Teste",
        category=Ticket.Category.BUG,
        priority=Ticket.Priority.MEDIUM,
        status=Ticket.Status.OPEN,
        requester=user,
    )

    # close
    client.post(f"/tickets/{ticket.id}/toggle-status/", follow=True)
    ticket.refresh_from_db()
    assert ticket.status == Ticket.Status.CLOSED

    client.post(f"/tickets/{ticket.id}/toggle-status/", follow=True)
    ticket.refresh_from_db()
    assert ticket.status == Ticket.Status.IN_PROGRESS


def test_logged_user_cant_comment_in_closed_ticket(client):
    create_user()
    client.login(username="erik", password="12345678")

    client.post(
        "/tickets/new/",
        data={
            "title": "Meu primeiro ticket",
            "description": "Descrição do ticket",
            "category": "BUG",
            "priority": "MEDIUM",
        },
        follow=True,
    )

    ticket = Ticket.objects.get()
    client.post(f"/tickets/{ticket.id}/toggle-status/", follow=True)
    ticket.refresh_from_db()
    assert ticket.status == Ticket.Status.CLOSED

    resp = client.post(
        f"/tickets/{ticket.id}/",
        data={"message": "Primeiro comentário"},
        follow=True,
    )

    assert resp.status_code == 200
    assert TicketComment.objects.count() == 0
