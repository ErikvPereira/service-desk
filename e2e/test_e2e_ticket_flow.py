import pytest
from django.contrib.auth import get_user_model

pytestmark = pytest.mark.django_db


@pytest.fixture
def user(db):
    User = get_user_model()
    return User.objects.create_user(username="erik", password="12345678")


@pytest.fixture
def live_server_url(live_server):
    return live_server.url


def test_e2e_login_create_ticket_and_comment(page, live_server_url, user):
    page.goto(f"{live_server_url}/login/")
    page.fill('input[name="username"]', "erik")
    page.fill('input[name="password"]', "12345678")
    page.click('button:has-text("Entrar")')
    page.wait_for_url("**/tickets/**")

    page.click("text=Novo chamado")
    page.fill('input[name="title"]', "Ticket E2E")
    page.fill('textarea[name="description"]', "Criado pelo Playwright")
    page.select_option('select[name="category"]', "BUG")
    page.select_option('select[name="priority"]', "MEDIUM")
    page.click('button:has-text("Criar")')

    page.click("text=Ticket E2E")

    page.fill('textarea[name="message"]', "Comentário E2E")
    page.click('button:has-text("Enviar")')

    page.wait_for_selector("text=Comentário E2E")
