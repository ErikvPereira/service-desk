## Service Desk (Django)
[![CI](https://github.com/ErikvPereira/service-desk/actions/workflows/tests.yml/badge.svg)](https://github.com/ErikvPereira/service-desk/actions/workflows/tests.yml)

Sistema simples de **controle de chamados (helpdesk/service desk)** feito em Django, com autenticação, tickets e comentários.  
Projeto focado em **boas práticas de mercado**: testes (pytest), E2E (Playwright), CI (GitHub Actions) e qualidade (ruff/black).

## Features
- Login/Logout
- Criar e listar tickets
- Detalhe do ticket
- Comentários em tickets
- Testes com pytest (fluxo de criação e comentários)
- Teste E2E com Playwright (login → criar ticket → comentar)
- CI no GitHub Actions (pytest + e2e)

## Stack
- Python 3.12
- Django
- SQLite (dev)
- Pytest + pytest-django
- Playwright + pytest-playwright
- Ruff + Black

## Rodar local (Windows)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## URLs locais: 
/tickets/
/login/

## Criar usuário:
```
python manage.py createsuperuser
```
## Testes:
```
pytest -q
pytest -q e2e
```

## Qualidade:
```
ruff check . --fix
black .
```