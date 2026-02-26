# fhir_bundle — Documentation

## Description

L'asset `fhir_bundle` traduit les données extraites par l'asset `traquer` en ressources FHIR R5 et les exporte sous forme de bundle XML. Il constitue la dernière étape du pipeline avant l'envoi vers un système tiers.

```
traquer (ClickHouse) → fhir_bundle (FHIR R5 XML) → [API / Serveur HDS]
```

---

## Structure des fichiers

```
vision/assets/traquer/
├── fhir_bundle.py   # Asset Dagster
├── mapping.py       # Fonctions de mapping FHIR
└── utils.py         # Fonctions utilitaires
```

---

## Fonctionnement actuel

À chaque partition journalière, l'asset :

1. Reçoit le DataFrame `traquer` (données patients, séjours, prélèvements, antibiogrammes)
2. Déduplique chaque entité et construit les ressources FHIR R5 (`Patient`, `Organization`, `Location`, `Encounter`, `Specimen`, `Observation`)
3. Assemble un Bundle FHIR de type `transaction`
4. Exporte le bundle au format XML dans `/tmp/fhir_bundles/bundle_fhir_<partition>.xml`

---

## Envoi vers une API ou un serveur distant HDS

### Prérequis

Avant d'envoyer des données vers un serveur distant hébergeant des données de santé (HDS), les points suivants doivent être validés :

- Le serveur cible est certifié **HDS** (Hébergeur de Données de Santé) conformément à la loi française
- Les données sont **pseudonymisées** ou le contrat d'hébergement couvre les données nominatives
- L'accès au serveur est sécurisé via **HTTPS/TLS**
- Les credentials (token, certificat) sont stockés dans un **coffre-fort** (Vault, variables d'environnement Dagster, secrets manager) et non en clair dans le code

---

### Option 1 — Envoi vers un serveur FHIR standard (HAPI, Azure Health, GCP Healthcare)

C'est l'option la plus directe. Le bundle FHIR est posté en une seule requête HTTP.

```python
import requests
import os

FHIR_SERVER_URL = os.environ["FHIR_SERVER_URL"]   # ex: https://mon-serveur-hds/fhir
FHIR_TOKEN      = os.environ["FHIR_TOKEN"]         # Bearer token ou API key

def send_bundle_to_fhir_server(bundle, context):
    headers = {
        "Content-Type": "application/fhir+xml",
        "Authorization": f"Bearer {FHIR_TOKEN}",
    }

    xml_output = bundle.model_dump_xml()
    if isinstance(xml_output, str):
        xml_output = xml_output.encode("utf-8")

    response = requests.post(
        f"{FHIR_SERVER_URL}",
        data=xml_output,
        headers=headers,
        timeout=60,
    )

    if response.status_code not in (200, 201):
        context.log.error(f"Erreur serveur FHIR : {response.status_code} — {response.text}")
        raise Exception(f"Échec de l'envoi du bundle FHIR : {response.status_code}")

    context.log.info(f"Bundle envoyé avec succès : {response.status_code}")
    return response
```

Dans `fhir_bundle.py`, remplacer `export_bundle_xml` par :

```python
send_bundle_to_fhir_server(bundle, context)
```

---

### Option 2 — Envoi vers une API REST personnalisée

Si le système cible expose une API REST propriétaire (et non un serveur FHIR natif), le bundle peut être envoyé en JSON.

```python
def send_bundle_to_api(bundle, context):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.environ['API_TOKEN']}",
    }

    payload = bundle.model_dump()  # dict Python → sérialisé en JSON

    response = requests.post(
        os.environ["API_URL"],
        json=payload,
        headers=headers,
        timeout=60,
    )

    if response.status_code not in (200, 201):
        context.log.error(f"Erreur API : {response.status_code} — {response.text}")
        raise Exception(f"Échec de l'envoi : {response.status_code}")

    context.log.info(f"Données envoyées avec succès : {response.status_code}")
```

---

### Option 3 — Envoi avec certificat client (mTLS)

Dans un contexte HDS, le serveur peut exiger une **authentification mutuelle TLS** (mTLS) avec un certificat client fourni par l'hébergeur.

```python
def send_bundle_mtls(bundle, context):
    cert_path = os.environ["FHIR_CLIENT_CERT"]   # chemin vers le certificat .pem
    key_path  = os.environ["FHIR_CLIENT_KEY"]    # chemin vers la clé privée .pem

    headers = {"Content-Type": "application/fhir+xml"}

    xml_output = bundle.model_dump_xml()
    if isinstance(xml_output, str):
        xml_output = xml_output.encode("utf-8")

    response = requests.post(
        os.environ["FHIR_SERVER_URL"],
        data=xml_output,
        headers=headers,
        cert=(cert_path, key_path),  # certificat client
        verify=True,                 # vérification du certificat serveur
        timeout=60,
    )

    if response.status_code not in (200, 201):
        context.log.error(f"Erreur mTLS : {response.status_code} — {response.text}")
        raise Exception(f"Échec envoi mTLS : {response.status_code}")

    context.log.info(f"Envoi mTLS réussi : {response.status_code}")
```

---

### Gestion des secrets dans Dagster

Ne jamais mettre les credentials en clair dans le code. Les déclarer comme variables d'environnement dans la configuration Dagster :

```yaml
# dagster.yaml ou workspace.yaml
env_vars:
  - FHIR_SERVER_URL
  - FHIR_TOKEN
  - FHIR_CLIENT_CERT
  - FHIR_CLIENT_KEY
```

Ou via les **Dagster Secrets** si tu utilises Dagster Cloud :

```python
# Accessible dans l'asset via
import os
url = os.environ["FHIR_SERVER_URL"]
```

---

### Garder l'export local en fallback

Il est recommandé de conserver l'export local en parallèle de l'envoi distant, comme filet de sécurité en cas d'échec réseau :

```python
# Exporter localement
export_bundle_xml(bundle, output_path)

# Puis envoyer au serveur distant
try:
    send_bundle_to_fhir_server(bundle, context)
except Exception as e:
    context.log.warning(f"Envoi distant échoué, fichier local disponible : {output_path}")
    raise
```

---

## Variables d'environnement requises

| Variable | Description | Obligatoire |
|---|---|---|
| `FHIR_SERVER_URL` | URL du serveur FHIR cible | Oui |
| `FHIR_TOKEN` | Bearer token d'authentification | Option 1 & 2 |
| `FHIR_CLIENT_CERT` | Chemin vers le certificat client `.pem` | Option 3 (mTLS) |
| `FHIR_CLIENT_KEY` | Chemin vers la clé privée `.pem` | Option 3 (mTLS) |
| `API_URL` | URL de l'API REST personnalisée | Option 2 |
| `API_TOKEN` | Token de l'API REST | Option 2 |

---

## Points de vigilance HDS

- Vérifier que le serveur cible est bien listé comme hébergeur certifié HDS sur [esante.gouv.fr](https://esante.gouv.fr)
- Ne jamais envoyer de données nominatives sur un environnement de test non certifié
- Conserver les logs d'envoi (date, partition, statut HTTP) pour l'auditabilité
- Prévoir une stratégie de retry en cas d'échec réseau (librairie `tenacity` ou mécanisme de retry Dagster)
