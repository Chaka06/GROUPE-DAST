# DAST NEWGEN'SPARK — Site Web Officiel

Site web professionnel Django pour l'agence numérique DAST NEWGEN'SPARK.

## Démarrage rapide

```bash
# 1. Créer l'environnement virtuel
python -m venv venv
source venv/bin/activate  # macOS/Linux

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Configurer les variables d'environnement
cp .env.example .env
# Editer .env avec vos valeurs

# 4. Appliquer les migrations
python manage.py migrate

# 5. Peupler les données initiales
python manage.py seed_data

# 6. Démarrer le serveur
python manage.py runserver
```

## Accès Administration

L'administration est accessible uniquement via : **http://localhost:8000/dast/**

Compte propriétaire par défaut (configurable dans .env) :
- Identifiant : `dast_owner`
- Mot de passe : défini dans `SUPER_ADMIN_PASSWORD`

## Configuration Supabase (Production)

1. Créer un projet sur [supabase.com](https://supabase.com)
2. Renseigner les variables `DB_*` dans `.env`
3. Pour le stockage media, activer `USE_SUPABASE_STORAGE=True`

## Variables d'environnement importantes

| Variable | Description |
|---|---|
| `SECRET_KEY` | Clé secrète Django (obligatoire en prod) |
| `DEBUG` | `False` en production |
| `DB_*` | Connexion PostgreSQL Supabase |
| `EMAIL_*` | Configuration SMTP |
| `CONTACT_EMAIL` | Email de réception des messages |

## Architecture

```
apps/
  accounts/   — Gestion des utilisateurs avec hiérarchie owner/admin
  core/       — Paramètres du site, partenaires, témoignages, FAQ
  home/       — Page d'accueil
  services/   — Services et leurs détails
  portfolio/  — Réalisations et projets
  blog/       — Blog avec éditeur riche
  contact/    — Formulaire de contact
```
