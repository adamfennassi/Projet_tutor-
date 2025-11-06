# Ordonnancement sur Machines Parallèles

## Vue d'ensemble
Projet d'optimisation d'ordonnancement sur machines parallèles utilisant le solveur CP-SAT de Google OR-Tools. Comprend un générateur de jeux de données et des outils d'analyse.

## Fichiers du projet

### 1. model_machine_parallele.ipynb
Notebook principal contenant la classe Machine_Parallele avec toutes les méthodes.

#### Méthodes disponibles :

Solveur principal
- __init__() - Initialiser et résoudre le problème

Récupération de données
- get_schedule() - Obtenir les informations complètes
- get_machine_utilization() - Calculer l'utilisation des machines
- get_critical_path() - Identifier les tâches critiques
- get_makespan() - Obtenir la durée totale

Analyse et rapports
- print_start_date() - Afficher les dates de début
- print_machine_assignments() - Afficher l'affectation tâches-machines
- print_order() - Afficher l'ordre chronologique
- print_utilization() - Afficher l'utilisation des machines
- print_critical_tasks() - Afficher les tâches critiques
- print_summary() - Rapport complet

Export et visualisation
- export_to_dataframe() - Exporter vers pandas DataFrame
- visualize_gantt() - Créer un diagramme de Gantt

### 2. generator.py
Générateur de jeux de données pour créer des cas de test et des benchmarks.

#### Classe SchedulingDatasetGenerator - Méthodes :

- generate_task_pair() - Générer une paire prédécesseur-successeur
- generate_dataset() - Générer un jeu de données complet
- tasks_to_csv() - Exporter vers fichier CSV
- load_from_csv() - Charger depuis un fichier CSV
- generate_multiple_datasets() - Générer plusieurs jeux de données
- print_dataset_stats() - Afficher les statistiques

#### Paramètres :
- num_pairs - Nombre de paires de tâches (total tâches = paires × 2)
- num_machines - Nombre de machines disponibles
- min_duration / max_duration - Plage de durée des tâches
- time_horizon - Fenêtre temporelle totale
- slack_factor - Marge (0.0=serré, 1.0=lâche)

### 3. Fichiers supports

- quick_example.py - Exemple d'intégration rapide
- test_solver_with_generated_data.py - Script de test complet
- USAGE_GUIDE.md - Documentation détaillée

## Démarrage rapide

### Utilisation de base

```python
from ortools.sat.python import cp_model
from collections import namedtuple
from generator import SchedulingDatasetGenerator

# Créer taskInfo namedtuple
taskInfo = namedtuple("taskInfo", ["duration", "predecessors", "relase_date", "due_date"])

# Générer un jeu de données
generator = SchedulingDatasetGenerator(seed=42)
tasks, machines = generator.generate_dataset(num_pairs=5, num_machines=3)

# Résoudre
solver = Machine_Parallele(taskInfo, tasks, machines)

# Voir les résultats
solver.print_summary()
```

### Générer et sauvegarder des jeux de données

```python
generator = SchedulingDatasetGenerator()

# Jeu de données unique
tasks, machines = generator.generate_dataset(num_pairs=4, num_machines=2)
generator.tasks_to_csv(tasks, machines, "my_dataset.csv")

# Plusieurs jeux de données
generator.generate_multiple_datasets(
    num_datasets=10,
    base_filename="test",
    num_pairs=5,
    num_machines=3
)
```

### Charger depuis CSV

```python
# Charger un jeu de données
tasks, machines = generator.load_from_csv("dataset.csv")

# Résoudre
solver = Machine_Parallele(taskInfo, tasks, machines)
solver.print_summary()
```

## Niveaux de difficulté des jeux de données

### Facile (taux de succès élevé)
```python
tasks, machines = generator.generate_dataset(
    num_pairs=3,
    num_machines=4,
    slack_factor=0.6
)
```

### Moyen (défi modéré)
```python
tasks, machines = generator.generate_dataset(
    num_pairs=5,
    num_machines=3,
    slack_factor=0.3
)
```

### Difficile
```python
tasks, machines = generator.generate_dataset(
    num_pairs=8,
    num_machines=2,
    slack_factor=0.1
)
```

## Fonctionnalités d'analyse

### Utilisation des machines
Mesure l'efficacité d'utilisation des machines :
- Temps de travail total par machine
- Temps d'inactivité par machine
- Pourcentage d'utilisation

### Analyse du chemin critique
Identifie les tâches avec marge minimale (risque de retard)

### Visualisation Gantt
Chronologie visuelle de l'exécution des tâches sur les machines

### Export vers DataFrame
Export des résultats pour analyse ou machine learning

## Format CSV

```csv
task_name,duration,predecessors,release_date,due_date
task_a_1,101,task_a_2,46,162
task_a_2,34,none,12,164
...
MACHINES,"m_1,m_2,m_3",,,
```

## Prérequis

```bash
pip install ortools pandas matplotlib
```

## Exemple de flux de travail

1. Générer des données de test
   ```bash
   python generator.py
   ```

2. Charger dans le notebook
   ```python
   tasks, machines = generator.load_from_csv("dataset.csv")
   ```

3. Résoudre le problème
   ```python
   solver = Machine_Parallele(taskInfo, tasks, machines)
   ```

4. Analyser les résultats
   ```python
   solver.print_summary()
   solver.visualize_gantt()
   df = solver.export_to_dataframe()
   ```

## Cas d'utilisation

1. Tests de performance du solveur - Générer divers jeux de données pour benchmarker
2. Machine Learning - Exporter les résultats pour entraîner des modèles ML
3. Planification de production - Optimisation réelle d'ordonnancement
4. Recherche académique - Expériences d'ordonnancement reproductibles
5. Comparaison d'algorithmes - Comparer différentes approches d'ordonnancement

## Concepts clés

### Paires de tâches
Chaque jeu de données se compose de paires de tâches où :
- Tâche 2 est le prédécesseur (sans dépendances)
- Tâche 1 est le successeur (dépend de Tâche 2)
- Modélise des scénarios réels comme préparation→exécution, setup→traitement

### Contraintes
- Release Date : date de début au plus tôt
- Due Date : date d'achèvement au plus tard
- Précédence : les successeurs attendent les prédécesseurs
- Non-chevauchement : une tâche par machine à la fois
- Affectation machine : chaque tâche assignée à exactement une machine

### Fonction objectif
Minimiser la somme des dates de début (encourage achèvement précoce)

## Dépannage

Aucune solution réalisable trouvée ?
- Augmenter slack_factor
- Ajouter plus de machines
- Réduire le nombre de paires de tâches
- Augmenter time_horizon

Trop facile ?
- Diminuer slack_factor
- Réduire le nombre de machines
- Augmenter le nombre de paires de tâches

## Prochaines étapes

1. Exécuter python generator.py pour voir la sortie exemple
2. Ouvrir model_machine_parallele.ipynb pour tester le solveur
3. Lire USAGE_GUIDE.md pour la documentation détaillée
4. Exécuter quick_example.py pour des exemples d'intégration
5. Utiliser test_solver_with_generated_data.py pour les tests complets

---

Version : 1.0
Dernière mise à jour : Novembre 2025

