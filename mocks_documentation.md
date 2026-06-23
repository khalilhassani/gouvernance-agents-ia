# Documentation des Mocks - Plateforme de Validation des Agents IA

Ce document décrit le fonctionnement et la structure des simulations et mocks implémentés dans l'atelier pour permettre l'exécution hors ligne et continue dans la pipeline CI/CD.

## 1. Simulation d'Agent IA (`agent_service.py`)

Pour éviter d'exposer des clés d'API sensibles dans le code source ou de faire dépendre le succès des tests de la disponibilité d'API externes (comme Groq ou OpenAI), le service d'agent est simulé.

### Fonctionnement du Mock :
*   **Classification d'Intention** : Analyse l'entrée utilisateur via un dictionnaire de mots-clés (`demande_document`, `reclamation`, `question_sensible`, `erreur_volontaire`) et lui attribue une intention avec un score de confiance simulé.
*   **Lookup Table de Tests (MAPPED_RESPONSES)** : Pour assurer la conformité absolue des tests nominaux, l'agent utilise une table de correspondance associant les 20 entrées du Golden Set à des réponses conformes, simulées et déterministes.
*   **Simulateur d'erreurs** : Pour tester la réactivité du validateur aux failles ou comportements anormaux, certaines entrées (comme `sans_politeness` ou `avec_hallucination`) renvoient des réponses violant délibérément les règles de conformité.

---

## 2. Moteur de Validation de Conformité (`conformity.py`)

Le validateur vérifie de manière automatisée la conformité de chaque réponse selon plusieurs règles d'évaluation.

### Règles de Scoring :
1.  **Vérification de l'Intention (-30 pts si incorrect)** : Assure que le but détecté par l'agent est cohérent avec l'attente métier.
2.  **Mots clés obligatoires (-15 pts par mot manquant)** : Par exemple, pour l'acte de naissance, la présence de "Wathiqa" ou "bureau d'état civil" est requise.
3.  **Mots clés interdits (-20 pts par mot trouvé)** : Détecte les termes indésirables comme "erreur", "impossible" ou "invalide" sur les canaux nominaux.
4.  **Ton E-Gov (-10 pts si absent)** : Assure que le message commence par une salutation polie ("Bonjour", "Monsieur/Madame").
5.  **Détection d'Hallucinations (-20 pts si trouvé)** : Repère les fuites d'erreurs logicielles ou les placeholders comme `[placeholder]`, `{variable}` ou `error 500`.

---

## 3. Avantages pour la CI/CD

Grâce à cette approche par mock déterministe :
*   **Zéro Coût** : Aucun token API payant n'est consommé lors des commits.
*   **Rapidité (2 secondes)** : Les tests s'exécutent instantanément en mémoire au lieu d'attendre les délais réseau des LLM.
*   **100% Déterministe** : Aucun risque de faux négatif dû à la variabilité des réponses de l'IA générative réelle.
