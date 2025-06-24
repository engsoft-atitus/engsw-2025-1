FROM python:3.11-slim

ENV DJANGO_DEBUG=False
# Instala dependências básicas e adiciona o repositório da Microsoft
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    apt-transport-https \
    && curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > /etc/apt/trusted.gpg.d/microsoft.gpg \
    && curl https://packages.microsoft.com/config/debian/11/prod.list | tee /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql17 unixodbc-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Define diretório de trabalho
WORKDIR /app

# Copia os arquivos do projeto
COPY . .

# Instala dependências Python
RUN pip install --upgrade pip && pip install -r requirements.txt

RUN python manage.py collectstatic --noinput
# Expõe a porta 8000
EXPOSE 8000

# Comando para iniciar o servidor com Gunicorn
CMD ["gunicorn", "django_project.wsgi:application", "--bind", "0.0.0.0:8000"]
