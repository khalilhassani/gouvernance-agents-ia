# Livrables de l'Exercice Pratique (Lab) - Déploiement d'Agents IA

Ce document contient l'ensemble des livrables requis pour la complétion du Lab dans l'environnement "antigravity".

---

## 1. Agent Card

L'**Agent Card** ci-dessous documente les spécifications techniques, opérationnelles et de sécurité de notre agent IA citoyen.

| Champ | Description / Spécification |
| :--- | :--- |
| **Nom de l'agent** | **Assistant Citoyen E-Gov** (e-Gov Citizen Assistant) |
| **Description** | Agent conversationnel conçu pour assister les citoyens dans leurs démarches administratives, recueillir les réclamations et réorienter de manière sécurisée les requêtes sensibles. |
| **Modèle utilisé** | **Gemini 1.5 Flash** (Production) / **Simulateur déterministe d'intentions** `agent_service.py` (Validation CI/CD). |
| **Entrées (Inputs)** | Message textuel libre saisi par le citoyen (ex. demande d'acte de naissance, dépôt de plainte, question sur les élections). |
| **Sorties (Outputs)** | Objet JSON structuré contenant :<br>- `response` (str) : Réponse textuelle formulée et polie.<br>- `intent` (str) : Catégorie d'intention détectée (`demande_document`, `reclamation`, `question_sensible`, `inquiry_general`).<br>- `confidence` (float) : Score de confiance de la classification (0.00 à 1.00).<br>- `tokens_used` (int) : Nombre de tokens consommés.<br>- `latency_ms` (int) : Temps de traitement en millisecondes. |
| **Dépendances clés** | - **FastAPI v0.110.0+** (Framework API)<br>- **Uvicorn v0.28.0+** (Serveur ASGI)<br>- **Pydantic v2.0+** (Validation des schémas de données)<br>- **Pytest v8.0+** (Exécution des tests de conformité)<br>- **Python 3.12** (Runtime principal) |
| **Limites de Sécurité & Guardrails** | 1. **Neutralité Politique** : Interdiction d'émettre des avis politiques ou électoraux. Redirection systématique vers l'Instance Nationale de Probité et de Lutte contre la Corruption (INPLC).<br>2. **Ton de Service Public** : Obligation d'inclure des formules de politesse administratives ("Bonjour", "Monsieur/Madame").<br>3. **Protection Infrastructure** : Masquage total des logs système système/erreurs système (`Fatal error`, `Database exception`) dans les réponses adressées aux citoyens.<br>4. **Prévention des Hallucinations** : Détection et blocage des chaînes non résolues comme `[placeholder]` ou `{variable}` avant envoi. |

---

## 2. Versionnement Git

Voici la séquence exacte des commandes Git à exécuter en ligne de commande pour versionner les prompts, les fichiers de configuration, le code source et créer le tag stable `v1.0.0`.

```bash
# 1. Initialiser le dépôt Git (si ce n'est pas déjà fait)
git init

# 2. Configurer l'identité de l'utilisateur pour le commit
git config --global user.name "Ingénieur DevOps"
git config --global user.email "devops@e-gov.ma"

# 3. Ajouter les configurations d'intégration continue (CI/CD)
git add .github/workflows/ci.yml

# 4. Ajouter les fichiers sources de l'agent, des modèles et du validateur
git add backend/app/main.py
git add backend/app/services/agent_service.py
git add backend/app/validators/conformity.py
git add backend/app/routes/agent.py backend/app/routes/tests.py backend/app/routes/workflow.py

# 5. Ajouter les fichiers de définition de tests (Prompts, Golden Set de 20 cas)
git add backend/app/tests_engine/engine.py
git add workflows/workflow_export.json

# 6. Ajouter les documentations et dépendances
git add backend/requirements.txt
git add README.md mocks_documentation.md test_report.md

# 7. Effectuer le commit de la version stable v1.0.0
git commit -m "feat: initial release of e-gov citizen assistant agent v1.0.0 with automated validation suite and CI pipeline"

# 8. Créer le tag de version v1.0.0
git tag -a v1.0.0 -m "Release v1.0.0 : Version initiale certifiée par la suite de tests de conformité (score 91.25%)"

# 9. Pousser les commits et le tag vers le dépôt distant (ex. GitHub/GitLab)
# git branch -M main
# git remote add origin <URL_DEPOT>
# git push -u origin main
# git push origin v1.0.0
```

---

## 3. Runbook Opérationnel

Ce runbook décrit les procédures standard d'exploitation pour le maintien en conditions opérationnelles (MCO) de l'agent.

### 3.1 Gestion des Incidents (Détection et Triage)

L'objectif de cette procédure est d'identifier rapidement toute dérive comportementale ou technique de l'agent et de qualifier sa sévérité.

#### A. Métriques de Supervision (Indicateurs Clés - SLIs)
*   **Taux d'Erreur API (5xx)** : Pourcentage d'appels à `/api/agents/run` se soldant par une erreur HTTP 500 ou 503.
*   **Latence de Réponse (p95)** : Temps mis par l'agent pour répondre aux sollicitations (seuil critique : > 500 ms).
*   **Score de Conformité Continuous Testing** : Score calculé par `conformity.py` sur les requêtes réelles ou la suite de validation (seuil critique : < 80.0%).
*   **Taux d'Hallucinations/Leaks** : Présence de mots interdits (`[placeholder]`, `{variable}`, `fatal error`) dans les réponses de production.

#### B. Matrice de Triage des Incidents
*   **Priorité 1 (P1) - Critique** :
    *   *Symptômes* : Service totalement indisponible (HTTP 503), temps de réponse > 2s sur 5 minutes consécutives, ou fuites répétées d'erreurs techniques (`Fatal error`) exposant l'infrastructure.
    *   *Action* : Déclenchement immédiat du **Kill-Switch (Procédure 3.2)**.
*   **Priorité 2 (P2) - Majeur** :
    *   *Symptômes* : Détection de réponses violant les règles de neutralité politique (ex. commentaires sur les fraudes électorales) ou absence systématique de formules de salutation (ton impoli).
    *   *Action* : Triage du prompt système et planification d'un correctif immédiat ou d'un **Rollback (Procédure 3.3)**.
*   **Priorité 3 (P3) - Mineur** :
    *   *Symptômes* : Augmentation légère de la latence moyenne (p50 > 250ms) ou baisse marginale du score de confiance de classification d'intention.
    *   *Action* : Monitoring renforcé, analyse des logs d'exécution hors ligne.

---

### 3.2 Procédure de "Kill-Switch" (Arrêt d'Urgence)

En cas de comportement dangereux, d'hallucinations majeures ou de compromission de l'agent, suivez l'une de ces méthodes pour couper le service instantanément.

#### Méthode A : Mode Maintenance Applicatif (Recommandé)
Le serveur FastAPI dispose d'un flag d'isolation de l'agent.
1. Se connecter au serveur de production.
2. Définir la variable d'environnement bloquante pour rediriger les flux de l'agent vers un message statique d'attente :
   ```bash
   # Sous Windows PowerShell :
   [System.Environment]::SetEnvironmentVariable("AGENT_STATUS", "maintenance", "Machine")
   # Sous Linux / Bash :
   export AGENT_STATUS="maintenance"
   ```
3. Redémarrer le serveur d'application :
   ```bash
   # Commande de redémarrage du service
   systemctl restart e-gov-backend.service
   ```
4. L'agent répondra désormais automatiquement par un message prédéfini : *"Notre assistant en ligne fait actuellement l'objet d'une maintenance technique. Pour toute urgence, veuillez nous contacter par téléphone au 3737."*

#### Méthode B : Arrêt Brutal du Service (Docker / Systemd)
Si l'application ne répond plus ou si l'API est compromise :
```bash
# Si déployé via Docker :
docker stop e-gov-agent-container

# Si déployé via Service Systemd Linux :
sudo systemctl stop e-gov-backend
```

---

### 3.3 Procédure de "Rollback" (Retour Arrière)

Si le déploiement de la version `v1.0.0` (ou d'une mise à jour ultérieure) introduit des régressions majeures non détectées par la CI/CD, appliquez cette procédure pour restaurer l'état stable précédent.

#### Étape 1 : Identification de la version stable
Consulter l'historique des tags Git pour identifier la dernière version stable validée (ex. `v0.9.0` ou le tag stable précédent).

#### Étape 2 : Retour arrière sur le dépôt Git de déploiement
```bash
# 1. Récupérer toutes les références de tags
git fetch --tags

# 2. Basculer le code vers le tag de la version stable précédente (ex: v0.9.5-stable)
git checkout tags/v0.9.5-stable

# 3. Créer une branche de hotfix temporaire pour acter le rollback
git checkout -b rollback-to-v0.9.5
```

#### Étape 3 : Déploiement et Reconstruction
Reconstruire et relancer l'application avec le code de la version stable restaurée.
```bash
# Si exécution par conteneur Docker :
docker build -t e-gov-agent:rollback -f backend/Dockerfile .
docker stop e-gov-agent-container
docker run -d --name e-gov-agent-container -p 8000:8000 e-gov-agent:rollback

# Si exécution en local/processus Python direct :
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
```

#### Étape 4 : Validation Post-Rollback
Vérifier impérativement le bon fonctionnement avant réouverture au public :
1. Exécuter la suite complète de tests de conformité :
   ```bash
   python -m pytest backend/app/tests/
   ```
2. Valider l'état du serveur de validation :
   ```bash
   curl -I http://127.0.0.1:8000/health
   ```
   *(La réponse doit renvoyer un statut `HTTP 200 OK` avec `{"status": "healthy"}`).*
