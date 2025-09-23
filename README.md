# Library API - Projet 5BDD

Une API de gestion de bibliothèque en ligne développée avec FastAPI, connectée à une base de données Oracle. Ce projet a été réalisé dans le cadre du mini-projet 5BDD (Introduction aux structures BDD, Data et API).

## Objectifs du projet
- Structurer une base de données Oracle sécurisée.
- Développer une API REST pour interagir avec la base.
- Mettre en place des migrations avec Alembic pour gérer l’évolution du schéma.
- Proposer une documentation interactive avec Swagger.
- Démontrer les fonctionnalités principales : gestion des utilisateurs, des livres et des emprunts.

## Technologies utilisées
- Base de données : Oracle XE 21c
- Backend : FastAPI (Python 3.11)
- ORM : SQLAlchemy
- Migrations : Alembic
- Validation : Pydantic
- Conteneurisation : Docker & Docker Compose

## Installation et lancement
1. Cloner le projet  
(git clone https://github.com/Mr10Wick/5BDD_library-api.git && cd 5BDD_library-api)  

2. Lancer avec Docker  
(docker compose up -d --build)  

3. Vérifier que l’API est en ligne  
(curl -i http://localhost:8000/health)  

4. Accéder à la documentation Swagger  
http://localhost:8000/docs  

## Fonctionnalités principales
### Gestion des utilisateurs
- Inscription (/auth/register)
- Connexion avec JWT (/auth/login)
- Profil utilisateur (/users/me)
- Historique des emprunts (/users/me/loans/history)

### Gestion des livres
- Ajouter, modifier, supprimer des livres
- Rechercher par titre, auteur ou genre
- Visualiser les détails d’un livre

### Gestion des emprunts
- Emprunter un livre (si disponible)
- Retourner un livre
- Consulter l’historique complet des emprunts

## Exemples de tests (via cURL)
### Inscription
(curl -i -X POST "http://localhost:8000/auth/register" -H "Content-Type: application/json" -d '{"name":"Bob","email":"bob@example.com","phone":"0611111111","password":"secret123"}')  

### Connexion (token)
(TOKEN=$(curl -s -X POST "http://localhost:8000/auth/login" -H "Content-Type: application/json" -d '{"email":"bob@example.com","password":"secret123"}' | jq -r .access_token) && echo $TOKEN)  

### Ajouter un livre
(curl -i -X POST "http://localhost:8000/books" -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -d '{"title":"Dune","author":"Frank Herbert","genre":"SF"}')  

### Emprunter un livre
(curl -i -X POST "http://localhost:8000/loans/borrow" -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -d '{"book_id":1}')  

### Retourner un livre
(curl -i -X POST "http://localhost:8000/loans/return" -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -d '{"loan_id":1}')  

## Améliorations futures
- Ajout d’un rôle administrateur (gestion avancée des livres et utilisateurs).
- Gestion des pénalités de retard.
- Ajout de tests unitaires et intégration continue.
- Déploiement sur un service cloud.

## Documentation et suivi
Pour la documentation, Swagger est intégré automatiquement avec FastAPI et disponible à l’adresse (http://localhost:8000/docs). Cela permet de tester toutes les routes facilement. Le projet a été suivi et versionné avec GitHub, ce qui a permis un travail collaboratif et un suivi clair des versions.

## Conclusion
Ce projet a permis de mettre en place une API fonctionnelle connectée à Oracle, avec gestion des utilisateurs, des livres et des emprunts. Il illustre la mise en pratique des notions de bases de données, ORM, migrations et API REST. Ce travail constitue une base solide pour de futures améliorations et un déploiement à grande échelle.

## Auteurs
Projet réalisé dans le cadre de 5BDD - Mini projet et soutenance. Travail en binôme avec suivi via GitHub.

