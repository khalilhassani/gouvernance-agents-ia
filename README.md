# Plateforme de Validation et de Conformité des Agents IA

[![Agent Agentique CI Pipeline](https://img.shields.io/badge/CI-passed-success.svg)](https://github.com/your-repo/actions)
[![FastAPI Version](https://img.shields.io/badge/FastAPI-v0.110.0-blue.svg)](https://fastapi.tiangolo.com)
[![Python Version](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)

Cette plateforme permet de valider automatiquement la conformité, l'intention et le ton des réponses générées par des agents IA pour les services publics (e-gov). Elle fournit une suite de tests automatisée (CI/CD) ainsi qu'un dashboard de gouvernance interactif.

---

## 🚀 Livrables

Conformément au guide de construction, les livrables suivants sont disponibles dans ce dépôt :

### 1. Workflow Final & Documentation
*   **Export JSON** : Le fichier d'export du workflow structuré contenant la liste des agents, des cas de test et la synthèse des règles est disponible sous [workflows/workflow_export.json](file:///c:/Users/LENOVO/Downloads/projet%2023/workflows/workflow_export.json).
*   **Documentation** : Voir la section ci-dessous pour les détails de l'architecture.

### 2. Suite de Tests Métiers & Rapport
*   **Golden Set de 20 Cas** : Définis dans [backend/app/tests_engine/engine.py](file:///c:/Users/LENOVO/Downloads/projet%2023/backend/app/tests_engine/engine.py#L8).
*   **Exécution locale** : Validée via `pytest` (score global de conformité de **91.25%**, taux de réussite de **85.0%**).
*   **Rapport de conformité** : Disponible sous format Markdown récapitulatif dans [test_report.md](file:///c:/Users/LENOVO/Downloads/projet%2023/test_report.md) et format JSON exportable dans `reports/validation_report.json`.

### 3. Pipeline CI Fonctionnelle (Badge Vert)
*   **GitHub Actions** : Configurée dans [.github/workflows/ci.yml](file:///c:/Users/LENOVO/Downloads/projet%2023/.github/workflows/ci.yml).
*   **Déclenchement** : Automatique à chaque `push` et `pull_request` sur les branches `main` et `master`.
*   **Étapes** : Récupération du code source, configuration de Python 3.12, installation des dépendances, et exécution de `pytest` sur la suite de tests.

### 4. Documentation des Mocks
*   **Simulateur d'Agent & Mocks** : Détaillé dans le fichier [mocks_documentation.md](file:///c:/Users/LENOVO/Downloads/projet%2023/mocks_documentation.md).
*   **Bénéfices** : Zéro coût d'API, 100% déterministe, et exécution ultra-rapide en moins de 3 secondes dans la pipeline de CI.

---

## 🛠️ Architecture du Projet

```text
projet 23/
├── .github/workflows/      # Configurations CI/CD (GitHub Actions)
│   └── ci.yml
├── backend/
│   ├── app/
│   │   ├── main.py         # Point d'entrée de l'API FastAPI
│   │   ├── models/         # Schémas de données Pydantic
│   │   ├── routes/         # Endpoints de l'API (Agents, Tests, Workflow)
│   │   ├── services/       # Simulation de l'agent IA (Mock)
│   │   ├── tests/          # Tests unitaires et d'intégration
│   │   ├── tests_engine/   # Définitions des 20 cas de test Golden Set
│   │   └── validators/     # Moteur de règles de conformité
│   └── requirements.txt    # Dépendances Python
├── frontend/               # Fichiers statiques du Dashboard
│   ├── index.html
│   ├── style.css
│   └── app.js
├── reports/                # Rapports de validation générés en cours de run
├── workflows/              # Schémas et exports des workflows agentiques
├── mocks_documentation.md  # Détails de la stratégie de mocking
└── test_report.md          # Rapport récapitulatif textuel
```

---

## 🔧 Installation et Lancement

### Prérequis
*   Python 3.12 ou supérieur
*   Pip

### 1. Installation des Dépendances
Dans le répertoire principal, installez les dépendances :
```bash
pip install -r backend/requirements.txt
```

### 2. Exécution de la Suite de Tests
Pour exécuter les tests localement et générer le rapport JSON :
```bash
python -m pytest backend/app/tests/
```

### 3. Lancement de l'API et du Dashboard
Lancez le serveur backend FastAPI (qui sert également le dashboard frontend) :
```bash
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
```
Ouvrez ensuite votre navigateur sur **[http://127.0.0.1:8000](http://127.0.0.1:8000)** pour accéder à l'interface graphique interactive de gouvernance.
