FROM python:3.11-slim-bookworm

WORKDIR /app

# Installation sécurisée des dépendances système (pour MySQL)
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    gcc \
    pkg-config \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

    #Copie des dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#Copie du reste du code
COPY . .

#Commande de démarrage
CMD ["gunicorn", "--bind", "127.0.0.1:8000", "projetsql.wsgi:application"]