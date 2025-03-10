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

1. **Clone le dépôt** :

   ```bash
   git clone https://github.com/ton_nom_utilisateur/FastAPI-SQL-Architecture.git
   cd FastAPI-SQL-Architecture
   ```

2. **Installe les dépendances** :

   ```bash
   poetry install
   ```

3. **Démarre les services avec Docker Compose** :

   ```bash
   docker compose up -d
   ```

4. **Lance l'application** :
   ```bash
   poetry run uvicorn api.api:app --reload
   ```

## Configuration

Les variables d'environnement nécessaires peuvent être configurées dans un fichier `.env` à la racine du projet. Exemple :

```env
DB_NAME=nom_de_la_base_de_donnees
DB_USER=utilisateur
DB_PASSWORD=mot_de_passe
DB_PORT=3306
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
