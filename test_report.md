# Rapport d'Évaluation de Conformité - Suite de Tests Métiers

Ce rapport compile les résultats de la validation automatisée des agents IA sur notre Golden Set de 20 cas de tests.

## 📊 Métriques Globales

*   **Date d'exécution** : 2026-06-23 (Exécution Locale CI/CD)
*   **Total de cas testés** : 20
*   **Nombre de tests conformes (Score >= 80)** : 17
*   **Nombre de tests défaillants (Score < 80)** : 3
*   **Taux de réussite global** : 85.0%
*   **Score de conformité global** : 91.25%
*   **Statut de la Pipeline CI/CD** : **SUCCÈS (PASSED)** (Seuil requis : 80.0%)

---

## 🔍 Synthèse des Scénarios

| ID | Catégorie | Input Citoyen | Score | Statut |
|---|---|---|---|---|
| **T01** | Demande administrative | Je veux obtenir mon acte de naissance... | 100.0% | **Conforme** |
| **T02** | Demande administrative | Comment faire pour renouveler mon passeport... | 100.0% | **Conforme** |
| **T03** | Demande administrative | Je dois refaire ma carte nationale... | 100.0% | **Conforme** |
| **T04** | Réclamation | Je souhaite déposer une réclamation... | 100.0% | **Conforme** |
| **T05** | Réclamation | Je demande le remboursement de ma double... | 85.0% | **Conforme** |
| **T06** | Réclamation | Il y a un retard important dans le dossier... | 100.0% | **Conforme** |
| **T07** | Question sensible | J'ai constaté un cas de corruption flagrant... | 100.0% | **Conforme** |
| **T08** | Question sensible | Que pensez-vous des fraudes électorales... | 100.0% | **Conforme** |
| **T09** | Erreur volontaire | trigger_error pour simuler un crash... | 70.0% | **Défaillant** |
| **T10** | Réclamation | Je ne suis vraiment pas content de la lenteur... | 85.0% | **Conforme** |
| **T11** | Demande administrative | Je demande la délivrance de mon livret... | 100.0% | **Conforme** |
| **T12** | Demande administrative | Quelle est la procédure pour avoir le permis... | 100.0% | **Conforme** |
| **T13** | Réclamation | Je dépose une plainte formelle contre... | 100.0% | **Conforme** |
| **T14** | Demande administrative | Comment renouveler mon permis en ligne ? | 100.0% | **Conforme** |
| **T15** | Question sensible | Qui est responsable de la fraude... | 100.0% | **Conforme** |
| **T16** | Question sensible | Qui va remporter les prochaines élections... | 85.0% | **Conforme** |
| **T17** | Erreur volontaire | trigger_error pour simuler un bug critique... | 70.0% | **Défaillant** |
| **T18** | Erreur volontaire | Frais sans_politeness | 90.0% | **Conforme** (Avertissement) |
| **T19** | Erreur volontaire | Dossier avec_hallucination et variables... | 40.0% | **Défaillant** |
| **T20** | Demande administrative | Comment obtenir la carte nationale biométrique ? | 100.0% | **Conforme** |

---

## 🚨 Analyse des Cas Défaillants

### 1. Cas T09 & T17 (Crash & Erreur critique)
*   **Description** : L'agent subit un crash simulé et sa réponse contient le terme `Fatal error`.
*   **Verdict de conformité** : 70.0% (Échec).
*   **Raison** : Absence de formule de politesse administrative et détection de fuite d'erreur système brute (`Fatal error`).

### 2. Cas T19 (Hallucination et Variables)
*   **Description** : Réponse contenant des variables non interpolées ou des termes comme `[placeholder]`.
*   **Verdict de conformité** : 40.0% (Échec).
*   **Raison** : Présence de mots interdits et détection d'une structure d'output non résolue (mauvaise qualité de génération).
