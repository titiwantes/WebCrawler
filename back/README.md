## Fonctionnalités

- API RESTful construite avec FastAPI
- Authentification des utilisateurs
- Modèle de base de données SQL avec SQLAlchemy
- Migrations gérées avec Alembic
- Conteneurs Docker pour la base de données et Redis

## Prérequis

- Python 3.8 ou supérieur
- Docker et Docker Compose
- Poetry

## Installation

1. **Installe les dépendances** :

   ```bash
   poetry install
   ```

2. **Lance shell poetry**

   ```bash
   poetry shell
   ```

3. **Démarre les services avec Docker Compose** :

   ```bash
   docker compose up -d
   ```

4. **Lance l'application** :
   ```bash
   poetry run uvicorn api.main:app --reload
   ```

## Configuration

Les variables d'environnement nécessaires peuvent être configurées dans un fichier `.env` à la racine du projet. Exemple :

```env
DB_NAME=nom_de_la_base_de_donnees
DB_USER=utilisateur
DB_PASSWORD=mot_de_passe
DB_PORT=3306
REDIS_PORT=6379
```

## Migrations de la base de données

Pour appliquer les migrations, utilise la commande suivante :

```bash
poetry run alembic upgrade head
```

## Tests

Pour exécuter les tests, utilise :

```bash
poetry run pytest
```
