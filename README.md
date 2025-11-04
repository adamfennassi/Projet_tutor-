# Ordonnancement sur Machines Parallèles Non-Reliées
# Parallel Machine Scheduling Solver

## 🎯 Vue d'Ensemble / Overview
Ce projet fournit une solution complète pour l'optimisation de l'ordonnancement sur machines parallèles non-reliées utilisant le solveur CP-SAT de Google OR-Tools, avec des outils d'analyse complets et des capacités de génération de jeux de données.

This project provides a complete solution for parallel machine scheduling optimization using Google OR-Tools CP-SAT solver, with comprehensive analysis tools and dataset generation capabilities.

## 📁 Fichiers du Projet / Project Files

### 1. **model_machine_parallele.ipynb**
Notebook principal contenant la classe `Machine_Parallele` avec toutes les méthodes.
Main notebook containing the `Machine_Parallele` solver class with all methods.

#### Méthodes Disponibles / Available Methods:

**Solveur Principal / Core Solver:**
- `__init__()` - Initialiser et résoudre le problème / Initialize and solve the scheduling problem

**Récupération de Données / Data Retrieval:**
- `get_schedule()` - Obtenir les informations complètes / Get complete scheduling information
- `get_machine_utilization()` - Calculer l'utilisation des machines / Calculate machine utilization stats
- `get_critical_path()` - Identifier les tâches critiques / Identify critical tasks
- `get_makespan()` - Obtenir la durée totale / Get total project completion time

**Analyse et Rapports / Analysis & Reporting:**
- `print_start_date()` - Afficher les dates de début / Print start times for all tasks
- `print_machine_assignments()` - Afficher l'affectation tâches-machines / Show task-to-machine assignments
- `print_order()` - Afficher l'ordre chronologique / Display chronological execution order
- `print_utilization()` - Afficher l'utilisation des machines / Print machine utilization statistics
- `print_critical_tasks()` - Afficher les tâches critiques / Show tasks with low slack
- `print_summary()` - Rapport complet / Comprehensive report of all metrics

**Export et Visualisation / Export & Visualization:**
- `export_to_dataframe()` - Exporter vers pandas DataFrame / Export schedule to pandas DataFrame
- `visualize_gantt()` - Créer un diagramme de Gantt / Create Gantt chart visualization

### 2. **generator.py**
Dataset generator for creating test cases and benchmarks.

#### `SchedulingDatasetGenerator` Class Methods:

- `generate_task_pair()` - Generate a single predecessor-successor task pair
- `generate_dataset()` - Generate complete dataset with multiple task pairs
- `tasks_to_csv()` - Export dataset to CSV file
- `load_from_csv()` - Load dataset from CSV file
- `generate_multiple_datasets()` - Batch generate datasets
- `print_dataset_stats()` - Display dataset statistics

#### Parameters:
- `num_pairs` - Number of task pairs (total tasks = pairs × 2)
- `num_machines` - Number of available machines
- `min_duration` / `max_duration` - Task duration range
- `time_horizon` - Total time window
- `slack_factor` - Deadline tightness (0.0=tight, 1.0=loose)

### 3. **Supporting Files**

- `quick_example.py` - Quick integration example
- `test_solver_with_generated_data.py` - Comprehensive testing script
- `USAGE_GUIDE.md` - Detailed usage documentation

## 🚀 Quick Start

### Basic Usage

```python
from ortools.sat.python import cp_model
from collections import namedtuple
from generator import SchedulingDatasetGenerator

# Create taskInfo namedtuple
taskInfo = namedtuple("taskInfo", ["duration", "predecessors", "relase_date", "due_date"])

# Generate dataset
generator = SchedulingDatasetGenerator(seed=42)
tasks, machines = generator.generate_dataset(num_pairs=5, num_machines=3)

# Solve
solver = Machine_Parallele(taskInfo, tasks, machines)

# View results
solver.print_summary()
```

### Generate and Save Datasets

```python
generator = SchedulingDatasetGenerator()

# Single dataset
tasks, machines = generator.generate_dataset(num_pairs=4, num_machines=2)
generator.tasks_to_csv(tasks, machines, "my_dataset.csv")

# Multiple datasets
generator.generate_multiple_datasets(
    num_datasets=10,
    base_filename="test",
    num_pairs=5,
    num_machines=3
)
```

### Load from CSV

```python
# Load dataset
tasks, machines = generator.load_from_csv("dataset.csv")

# Solve
solver = Machine_Parallele(taskInfo, tasks, machines)
solver.print_summary()
```

## 📊 Dataset Difficulty Levels

### Easy (High Success Rate)
```python
tasks, machines = generator.generate_dataset(
    num_pairs=3,
    num_machines=4,
    slack_factor=0.6
)
```

### Medium (Moderate Challenge)
```python
tasks, machines = generator.generate_dataset(
    num_pairs=5,
    num_machines=3,
    slack_factor=0.3
)
```

### Hard (Challenging)
```python
tasks, machines = generator.generate_dataset(
    num_pairs=8,
    num_machines=2,
    slack_factor=0.1
)
```

## 📈 Analysis Features

### Machine Utilization
Shows how efficiently machines are being used:
- Total work time per machine
- Idle time per machine
- Utilization percentage

### Critical Path Analysis
Identifies tasks with minimal slack (at risk of delays)

### Gantt Chart Visualization
Visual timeline of task execution across machines

### Export to DataFrame
Export results for further analysis or machine learning

## 💾 CSV Format

```csv
task_name,duration,predecessors,release_date,due_date
task_a_1,101,task_a_2,46,162
task_a_2,34,none,12,164
...
MACHINES,"m_1,m_2,m_3",,,
```

## 🔧 Requirements

```bash
pip install ortools pandas matplotlib
```

## 📝 Example Workflow

1. **Generate Test Data**
   ```bash
   python generator.py
   ```

2. **Load in Notebook**
   ```python
   tasks, machines = generator.load_from_csv("dataset.csv")
   ```

3. **Solve Problem**
   ```python
   solver = Machine_Parallele(taskInfo, tasks, machines)
   ```

4. **Analyze Results**
   ```python
   solver.print_summary()
   solver.visualize_gantt()
   df = solver.export_to_dataframe()
   ```

## 🎓 Use Cases

1. **Testing Solver Performance** - Generate diverse datasets to benchmark
2. **Machine Learning** - Export results to train ML models
3. **Production Planning** - Real-world scheduling optimization
4. **Academic Research** - Reproducible scheduling experiments
5. **Algorithm Comparison** - Compare different scheduling approaches

## 📚 Key Concepts

### Task Pairs
Each dataset consists of task pairs where:
- Task 2 is the predecessor (no dependencies)
- Task 1 is the successor (depends on Task 2)
- This models real-world scenarios like setup→execution, prep→processing, etc.

### Constraints
- **Release Date**: Earliest start time
- **Due Date**: Latest completion time
- **Precedence**: Successors wait for predecessors
- **No Overlap**: One task per machine at a time
- **Machine Assignment**: Each task assigned to exactly one machine

### Optimization Objective
Minimize the sum of start times (encourages early completion)

## 🔍 Troubleshooting

**No Feasible Solution Found?**
- Increase `slack_factor`
- Add more machines
- Reduce number of task pairs
- Increase `time_horizon`

**Too Easy?**
- Decrease `slack_factor`
- Reduce number of machines
- Increase number of task pairs

## 📧 Next Steps

1. Run `python generator.py` to see example output
2. Open `model_machine_parallele.ipynb` to test the solver
3. Read `USAGE_GUIDE.md` for detailed documentation
4. Run `quick_example.py` for integration examples
5. Use `test_solver_with_generated_data.py` for comprehensive testing

---

**Happy Scheduling! 🎉**
