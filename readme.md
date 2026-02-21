# Azure Dashboard

Dashboard terminal pour administrer un tenant Azure/Entra ID via Microsoft Graph API.

## Fonctionnalités
- Recherche de membres d'un groupe Entra ID
- Liste des utilisateurs inactifs depuis 90 jours

## Installation
pip install azure-identity requests rich

## Configuration
Crée un fichier `config.py` avec :
TENANT_ID     = "ton-tenant-id"
CLIENT_ID     = "ton-client-id"
CLIENT_SECRET = "ton-client-secret"

## Permissions requises (App Registration)
- Group.Read.All
- User.Read.All
- AuditLog.Read.All