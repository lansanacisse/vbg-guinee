# GBV Data Platform

Plateforme de gestion et de reporting des violences basées sur le genre en Guinée.

## Overview

Cette plateforme permet de:
- Collecter les déclarations de violences
- Générer des rapports statistiques
- Visualiser les données de manière sécurisée

## Stack Technologique

- **Backend**: Django REST Framework
- **Frontend**: Flask
- **Database**: PostgreSQL
- **Containerization**: Docker & Docker Compose

## Installation

### Prérequis
- Docker & Docker Compose
- Python 3.9+
- PostgreSQL 12+

### Démarrage rapide

```bash
# Cloner le repository
git clone https://github.com/lansanacisse/vbg-guinee.git
cd vbg-guinee

# Configuration
cp .env.example .env

# Lancer les services
docker-compose up -d
```

## Structure du Projet

```
gbv-data-platform/
├── backend/          # API Django REST
├── frontend/         # Interface Flask
├── database/         # Schémas et données initiales
├── docs/            # Documentation
└── docker-compose.yml
```

## Documentation

- [Architecture](docs/architecture.md)
- [Sécurité](docs/security.md)
- [API Reference](docs/api.md)

## Licence

Voir LICENSE pour plus de détails.