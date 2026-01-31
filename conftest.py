import os

# Necessário quando plugins/Playwright deixam um event loop ativo durante o setup do Django.
os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")
