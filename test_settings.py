from django_project.settings import *  # importa tudo do settings normal

# Usa SQLite em memória só para os testes
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}