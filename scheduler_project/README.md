# Planificateur de Tâches - Ordonnancement sur Machines Parallèles

Application web Django pour l'optimisation d'ordonnancement sur machines parallèles utilisant le solveur CP-SAT de Google OR-Tools.

---

## Table des Matières

1. [Vue d'ensemble](#vue-densemble)  
2. [Architecture du Projet](#architecture-du-projet)  
3. [Logique et Méthodes](#logique-et-méthodes)  
4. [Installation](#installation)  
5. [Utilisation](#utilisation)  
6. [Structure de la Base de Données](#structure-de-la-base-de-données)  
7. [Format CSV](#format-csv)  
8. [Personnalisation](#personnalisation)  
9. [Dépannage](#dépannage)  
10. [Performance](#performance)

---

## Vue d'Ensemble

Application web développée dans le cadre d'un projet tuteuré, permettant de résoudre des problèmes d'ordonnancement sur machines parallèles. Elle utilise le solveur CP-SAT de Google OR-Tools pour trouver des solutions optimales.

### Fonctionnalités Principales

- Import de fichiers CSV avec tâches et machines
- Saisie manuelle via formulaires
- Résolution automatique avec OR-Tools
- Visualisation graphique des résultats
- Export des rapports en PDF
- Interface web responsive  

### Technologies Utilisées

| Technologie | Version | Utilisation |
|--------------|----------|-------------|
| Django | 4.2+ | Framework web |
| OR-Tools | 9.7+ | Solveur d’optimisation |
| Bootstrap | 5.3 | Interface utilisateur |
| Matplotlib | 3.7+ | Graphiques Gantt |
| ReportLab | 4.0+ | Export PDF |
| Pandas | 2.0+ | Manipulation de données |
| SQLite | 3 | Base de données par défaut |

---

## Architecture du Projet

```
scheduler_project/
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── scheduler/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── solver.py
│   ├── pdf_export.py
│   ├── views.py
│   ├── urls.py
│   └── templates/scheduler/
│       ├── base.html
│       ├── index.html
│       ├── upload_csv.html
│       ├── manual_entry.html
│       ├── add_machines.html
│       ├── add_tasks.html
│       ├── schedule_detail.html
│       └── results.html
├── media/
│   ├── uploads/
│   └── samples/
├── manage.py
└── requirements.txt
```

---

## Logique et Méthodes

### Modèle de Données

**Schedule (Planning)**  
- name, created_at, status, makespan, objective_value  
- Relations : machines (1-N), tasks (1-N), uploaded_file (1-1)

**Machine**  
- name, schedule (FK)  
- assigned_tasks (post-résolution)

**Task**  
- name, duration, successor_name, release_date, due_date  
- assigned_machine, start_time, end_time, slack

### Solveur (scheduler/solver.py)

Le modèle utilise la **programmation par contraintes** via OR-Tools CP-SAT :
- Variables : start_time, affectation binaire tâche → machine  
- Contraintes :  
  - affectation unique  
  - non-chevauchement  
  - précédence (fin prédécesseur ≤ début successeur)  
  - respect des fenêtres temporelles  
- Objectif : minimiser la somme des dates de début (favorise la compacité et la réduction du makespan)

---

## Installation

### Prérequis
- Python 3.8+  
- pip

### Étapes d'installation

```powershell
# Naviguer vers le dossier du projet
cd "chemin/vers/scheduler_project"

# Installer les dépendances
pip install -r requirements.txt

# Initialiser la base de données
python manage.py makemigrations scheduler
python manage.py migrate

# Démarrer le serveur
python manage.py runserver
```

**Accès à l'application :**
- Application : http://127.0.0.1:8000/
- Interface admin : http://127.0.0.1:8000/admin/ (optionnel)

---

## Utilisation

### Créer un Planning via CSV
1. Créer un nouveau planning  
2. Télécharger un fichier CSV  
3. Cliquer sur "Télécharger et traiter"  
4. Résoudre le planning  
5. Visualiser les résultats et exporter en PDF

### Créer un Planning Manuellement
1. Créer un planning  
2. Saisir le nom  
3. Ajouter les machines  
4. Ajouter les tâches  
5. Lancer la résolution  
6. Consulter les résultats

### Interpréter les Résultats
- **Makespan** : durée totale du projet  
- **Valeur objectif** : somme des dates de début  
- **Slack** : marge avant l’échéance  
  - Vert (>5) : confortable  
  - Rouge (≤5) : critique

---

## Structure de la Base de Données

```
Schedule (1) ──< (*) Machine
Schedule (1) ──< (*) Task
Schedule (1) ──< (1) UploadedFile
Task (*) ──> (1) Machine
```

---

## Format CSV

### Structure

```csv
task_name,duration,successors,release_date,due_date
task_a_1,120,task_a_2,0,600
task_a_2,20,none,0,600
task_b_1,120,task_b_2,0,600
task_b_2,120,none,0,600

MACHINES,"m_a,m_b",,,
```

**Règles :**
1. Ligne d’en-tête obligatoire  
2. Utiliser "none" pour les tâches sans successeur  
3. Ligne vide avant la section MACHINES  
4. Machines entre guillemets, séparées par des virgules  
5. Encodage UTF-8 recommandé

---

## Personnalisation

### Couleurs
Modifiez `scheduler/templates/scheduler/base.html` :

```css
:root {
  --primary-color: #2c3e50;
  --secondary-color: #3498db;
  --success-color: #2ecc71;
  --danger-color: #e74c3c;
}
```

### Fonction Objectif
Adaptez la classe `Machine_Parallele` dans `scheduler/solver.py` pour modifier la stratégie d’optimisation.

---

## Dépannage

### Aucune solution trouvée
- Augmenter le nombre de machines  
- Diminuer les durées ou prolonger les échéances  
- Vérifier les dépendances entre tâches

### Erreur lors de l’import CSV
- Vérifier la présence des en-têtes  
- Vérifier la ligne MACHINES  
- S’assurer de l’encodage UTF-8

---

## Performance

| Taille | Tâches | Machines | Temps |
|--------|--------|-----------|-------|
| Petite | 6 | 4 | < 1 s |
| Moyenne | 10–20 | 3–5 | 1–5 s |
| Grande | 30–50 | 5–10 | 5–30 s |

**Recommandations :**  
- Cas idéal : 10–30 tâches, 3–10 machines  
- Limite pratique : environ 100 tâches, 20 machines

---

**Version :** 1.0  
**Dernière mise à jour :** Novembre 2025  
**Auteur :** Projet Tuteuré – Ordonnancement sur Machines Parallèles  
