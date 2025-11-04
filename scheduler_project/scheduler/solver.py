"""
Solver Service - Integrates OR-Tools solver with Django models
"""
from ortools.sat.python import cp_model
from collections import namedtuple
from .models import Schedule, Task, Machine
import io
import base64
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


# Define taskInfo structure
taskInfo = namedtuple("taskInfo", ["duration", "successors", "release_date", "due_date"])


class Machine_Parallele:
    """
    Classe pour résoudre le problème d'ordonnancement sur machines parallèles non-reliées.
    Utilise le solveur CP-SAT de OR-Tools pour optimiser l'affectation des tâches aux machines.
    """
    
    def __init__(self, taskInfo, tasks, machines):
        """
        Initialise le modèle d'ordonnancement.
        
        Paramètres:
            taskInfo: namedtuple définissant la structure des tâches
            tasks: dictionnaire des tâches {nom: taskInfo(duration, successors, release_date, due_date)}
            machines: liste des machines disponibles
        """
        self.taskInfo = taskInfo
        self.tasks = tasks 
        self.machines = machines

        # Créer le modèle CP-SAT
        self.model = cp_model.CpModel()

        # Variables de décision: temps de début de chaque tâche
        self.start_time_vars = {
            task_name: self.model.new_int_var_from_domain(
                cp_model.Domain.from_intervals([[task_info.release_date, task_info.due_date - task_info.duration]]),
                f"start_{task_name}"
            )
            for task_name, task_info in self.tasks.items()
        }

        # Variables booléennes: affectation des tâches aux machines
        self.machine_vars = {
            task_name: {
                machine: self.model.new_bool_var(f"{task_name}_on_{machine}") 
                for machine in self.machines
            }
            for task_name in self.tasks
        }

        # Variables d'intervalle pour la contrainte de non-chevauchement
        self.interval_vars = {
            task_name: {
                machine: self.model.new_optional_fixed_size_interval_var(
                    start=self.start_time_vars[task_name],
                    size=task_info.duration,
                    is_present=self.machine_vars[task_name][machine],
                    name=f"interval_{task_name}_on_{machine}"
                )
                for machine in self.machines
            }
            for task_name, task_info in self.tasks.items()
        }

        # CONTRAINTES
        
        # 1. Chaque tâche doit être affectée à exactement une machine
        for task_name, machine_dict in self.machine_vars.items():
            self.model.add_exactly_one(machine_dict.values())

        # 2. Non-chevauchement: les tâches sur la même machine ne peuvent pas se chevaucher
        for machine in self.machines:
            self.model.add_no_overlap([
                self.interval_vars[task_name][machine] 
                for task_name in self.tasks
            ])

        # 3. Contraintes de précédence: une tâche doit se terminer avant son successeur
        for task_name, task_info in self.tasks.items():
            if task_info.successors != "none":
                successor_name = task_info.successors
                task_end = self.start_time_vars[task_name] + task_info.duration
                self.model.Add(task_end <= self.start_time_vars[successor_name])

        # FONCTION OBJECTIF
        self.model.Minimize(
            sum(self.start_time_vars[task_name] for task_name in self.tasks)
        )
        
        # Résoudre le modèle
        self.solver = cp_model.CpSolver()
        self.status = self.solver.solve(self.model)
    
    def get_schedule(self):
        """
        Retourne l'ordonnancement complet sous forme de dictionnaire.
        """
        if self.status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            return None
        
        schedule = {}
        for task_name, task_info in self.tasks.items():
            start = self.solver.value(self.start_time_vars[task_name])
            end = start + task_info.duration
            
            # Trouver la machine affectée
            assigned_machine = None
            for machine in self.machines:
                if self.solver.value(self.machine_vars[task_name][machine]):
                    assigned_machine = machine
                    break
            
            slack = task_info.due_date - end
            
            schedule[task_name] = {
                'start': start,
                'end': end,
                'duration': task_info.duration,
                'machine': assigned_machine,
                'release_date': task_info.release_date,
                'due_date': task_info.due_date,
                'slack': slack,
                'successor': task_info.successors
            }
        
        return schedule
    
    def get_makespan(self):
        """Retourne le makespan (durée totale du projet)."""
        if self.status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            return None
        
        schedule = self.get_schedule()
        if not schedule:
            return None
        
        return max(info['end'] for info in schedule.values())
    
    def generate_gantt_chart(self):
        """
        Génère un diagramme de Gantt et retourne l'image en base64
        """
        if self.status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            return None
        
        schedule = self.get_schedule()
        if not schedule:
            return None
        
        # Palette de couleurs
        colors = plt.cm.tab20(range(20))
        
        def get_project_name(task_name):
            parts = task_name.rsplit('_', 1)
            if len(parts) == 2 and parts[1].isdigit():
                return parts[0]
            return task_name
        
        # Assigner couleurs aux projets
        projects = list(set(get_project_name(task) for task in schedule.keys()))
        project_colors = {project: colors[i % 20] for i, project in enumerate(sorted(projects))}
        
        # Créer la figure
        fig, ax = plt.subplots(figsize=(14, max(6, len(self.machines) * 1.5)))
        
        # Grouper par machine
        machine_tasks = {machine: [] for machine in self.machines}
        for task_name, info in schedule.items():
            machine_tasks[info['machine']].append((task_name, info))
        
        # Dessiner le diagramme
        yticks = []
        yticklabels = []
        
        for machine_idx, machine in enumerate(self.machines):
            y_pos = machine_idx
            tasks = sorted(machine_tasks[machine], key=lambda x: x[1]['start'])
            
            for task_name, info in tasks:
                project = get_project_name(task_name)
                task_color = project_colors[project]
                
                ax.barh(y_pos, info['duration'], left=info['start'], 
                       height=0.6, color=task_color, 
                       edgecolor='black', linewidth=1.5, alpha=0.85)
                
                ax.text(info['start'] + info['duration']/2, y_pos, task_name, 
                       ha='center', va='center', fontsize=9, fontweight='bold',
                       color='white', bbox=dict(boxstyle='round,pad=0.3', 
                       facecolor='black', alpha=0.3, edgecolor='none'))
            
            yticks.append(y_pos)
            yticklabels.append(machine)
        
        ax.set_yticks(yticks)
        ax.set_yticklabels(yticklabels, fontsize=11, fontweight='bold')
        ax.set_ylabel('Machines', fontsize=12, fontweight='bold')
        ax.set_xlabel('Time', fontsize=12, fontweight='bold')
        ax.set_title('Gantt Chart - Parallel Machine Scheduling', 
                    fontsize=14, fontweight='bold')
        
        ax.grid(axis='x', alpha=0.4, linestyle='--')
        ax.set_axisbelow(True)
        
        max_time = max(info['end'] for info in schedule.values())
        ax.set_xlim(0, max_time * 1.05)
        
        # Légende
        legend_patches = [
            mpatches.Patch(color=project_colors[proj], label=proj, alpha=0.85) 
            for proj in sorted(projects)
        ]
        ax.legend(handles=legend_patches, loc='upper right', fontsize=9, title='Projects')
        
        plt.tight_layout()
        
        # Convertir en base64
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode()
        plt.close(fig)
        
        return image_base64


def solve_schedule(schedule_id):
    """
    Résout un schedule Django et met à jour la base de données
    
    Args:
        schedule_id: ID du Schedule à résoudre
        
    Returns:
        tuple: (success: bool, message: str, gantt_chart: str or None)
    """
    try:
        schedule = Schedule.objects.get(id=schedule_id)
        
        # Récupérer les tâches et machines
        tasks_qs = schedule.tasks.all()
        machines_qs = schedule.machines.all()
        
        if not tasks_qs.exists():
            return False, "No tasks found in schedule", None
        
        if not machines_qs.exists():
            return False, "No machines found in schedule", None
        
        # Convertir en format attendu par le solver
        tasks_dict = {}
        for task in tasks_qs:
            tasks_dict[task.name] = taskInfo(
                duration=task.duration,
                successors=task.successor_name,
                release_date=task.release_date,
                due_date=task.due_date
            )
        
        machines_list = [m.name for m in machines_qs]
        
        # Résoudre
        solver = Machine_Parallele(taskInfo, tasks_dict, machines_list)
        
        if solver.status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            schedule.status = 'no_solution'
            schedule.save()
            return False, "No feasible solution found. Try adding more machines or relaxing constraints.", None
        
        # Récupérer la solution
        solution = solver.get_schedule()
        makespan = solver.get_makespan()
        
        # Mettre à jour la base de données
        schedule.status = 'solved'
        schedule.makespan = makespan
        schedule.objective_value = solver.solver.objective_value
        schedule.save()
        
        # Mettre à jour les tâches avec la solution
        for task in tasks_qs:
            if task.name in solution:
                info = solution[task.name]
                task.start_time = info['start']
                task.end_time = info['end']
                task.slack = info['slack']
                
                # Trouver la machine assignée
                machine_obj = machines_qs.get(name=info['machine'])
                task.assigned_machine = machine_obj
                task.save()
        
        # Générer le Gantt chart
        gantt_chart = solver.generate_gantt_chart()
        
        return True, "Schedule solved successfully!", gantt_chart
        
    except Schedule.DoesNotExist:
        return False, "Schedule not found", None
    except Exception as e:
        try:
            schedule.status = 'error'
            schedule.save()
        except:
            pass
        return False, f"Error solving schedule: {str(e)}", None


def parse_csv_file(file_path):
    """
    Parse un fichier CSV et retourne les tâches et machines
    
    Args:
        file_path: Chemin vers le fichier CSV
        
    Returns:
        tuple: (tasks_dict, machines_list) or (None, None) si erreur
    """
    import csv
    
    try:
        tasks_dict = {}
        machines_list = []
        
        with open(file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            
            for row in reader:
                if row['task_name'] == 'MACHINES':
                    machines_list = row['duration'].split(',')
                    break
                
                if row['task_name']:  # Ignorer les lignes vides
                    tasks_dict[row['task_name']] = {
                        'duration': int(row['duration']),
                        'successor_name': row['successors'],
                        'release_date': int(row['release_date']),
                        'due_date': int(row['due_date'])
                    }
        
        return tasks_dict, machines_list
        
    except Exception as e:
        print(f"Error parsing CSV: {e}")
        return None, None
