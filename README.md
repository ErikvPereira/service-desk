\# Service Desk (Django)



\## Rodar local

```bash

python -m venv .venv

\\# Windows

.\\\\.venv\\\\Scripts\\\\Activate.ps1

pip install -r requirements.txt

python manage.py migrate

python manage.py runserver

## E2E (Playwright)
```bash
pytest -q e2e
# ver o navegador
pytest -q e2e --headed



