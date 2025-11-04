"""
Générateur de Jeux de Données pour l'Ordonnancement sur Machines Parallèles
Dataset Generator for Parallel Machine Scheduling

Génère des jeux de données synthétiques avec 3 niveaux de difficulté:
- FACILE: Beaucoup de marge (slack élevé)
- MOYEN: Marge modérée
- DIFFICILE: Très peu de marge (contraintes serrées)
"""

import random
import csv
from collections import namedtuple
from typing import List, Dict, Tuple
from datetime import datetime


class SchedulingDatasetGenerator:
    """
    Générateur de jeux de données pour l'ordonnancement sur machines parallèles.
    Chaque projet consiste en une paire de tâches (task_X_1 -> task_X_2).
    """
    
    # Niveaux de difficulté prédéfinis
    FACILE = {
        'num_pairs': 3,          # 3 projets (6 tâches)
        'num_machines': 4,       # 4 machines
        'min_duration': 20,
        'max_duration': 80,
        'slack_factor': 0.6      # 60% de marge - BEAUCOUP de flexibilité
    }
    
    MOYEN = {
        'num_pairs': 5,          # 5 projets (10 tâches)
        'num_machines': 3,       # 3 machines
        'min_duration': 30,
        'max_duration': 100,
        'slack_factor': 0.3      # 30% de marge - Modéré
    }
    
    DIFFICILE = {
        'num_pairs': 8,          # 8 projets (16 tâches)
        'num_machines': 10,       # 10 machines
        'min_duration': 40,
        'max_duration': 120,
        'slack_factor': 0.05     # 5% de marge - TRÈS serré
    }
    
    def __init__(self, seed=None):
        """
        Initialise le générateur.
        
        Args:
            seed: Graine aléatoire pour la reproductibilité (None = aléatoire)
        """
        # Si aucune graine n'est fournie, utiliser l'heure actuelle pour la randomisation
        if seed is None:
            seed = int(datetime.now().timestamp() * 1000) % (2**32)
        
        random.seed(seed)
        self.current_seed = seed
        
        # Structure des données de tâche
        self.taskInfo = namedtuple("taskInfo", ["duration", "successors", "release_date", "due_date"])
    
    def generate_dataset(
        self,
        num_pairs: int = 5,
        num_machines: int = 3,
        min_duration: int = 20,
        max_duration: int = 100,
        slack_factor: float = 0.3,
        time_horizon: int = 1000
    ) -> Tuple[Dict, List[str]]:
        """
        Génère un jeu de données complet.
        
        Args:
            num_pairs: Nombre de paires de tâches (projets)
            num_machines: Nombre de machines disponibles
            min_duration: Durée minimale d'une tâche
            max_duration: Durée maximale d'une tâche
            slack_factor: Facteur de marge (0.0-1.0, plus petit = plus difficile)
            time_horizon: Horizon de temps total
            
        Returns:
            (dictionnaire_tâches, liste_machines)
        """
        tasks = {}
        
        # Générer les identifiants de projets: a, b, c, d, ...
        project_ids = [chr(97 + i) for i in range(num_pairs)]
        
        for project_id in project_ids:
            # Générer les durées des deux tâches du projet
            duration_1 = random.randint(min_duration, max_duration)
            duration_2 = random.randint(min_duration, max_duration)
            
            # Date de disponibilité de la première tâche
            release_1 = random.randint(0, time_horizon // 4)
            
            # La deuxième tâche peut commencer après la fin de la première
            min_start_2 = release_1 + duration_1
            release_2 = min_start_2
            
            # Calculer les échéances avec la marge (slack)
            total_duration = duration_1 + duration_2
            slack_time = int(total_duration * slack_factor)
            
            # Échéance pour task_1: doit permettre à task_2 de finir
            min_due_1 = release_1 + duration_1 + duration_2
            due_1 = min_due_1 + slack_time
            
            # Échéance pour task_2
            min_due_2 = release_2 + duration_2
            due_2 = min_due_2 + slack_time
            
            # S'assurer que les échéances restent dans l'horizon de temps
            due_1 = min(due_1, time_horizon)
            due_2 = min(due_2, time_horizon)
            
            # Créer les deux tâches du projet
            tasks[f"task_{project_id}_1"] = self.taskInfo(
                duration=duration_1,
                successors=f"task_{project_id}_2",  # task_2 est le successeur
                release_date=release_1,
                due_date=due_1
            )
            
            tasks[f"task_{project_id}_2"] = self.taskInfo(
                duration=duration_2,
                successors="none",  # Pas de successeur
                release_date=release_2,
                due_date=due_2
            )
        
        # Générer la liste des machines
        machines = [f"m_{i+1}" for i in range(num_machines)]
        
        return tasks, machines
    
    def generate_facile(self) -> Tuple[Dict, List[str]]:
        """Génère un jeu de données FACILE (beaucoup de marge)."""
        print("[FACILE] Generation d'un jeu de donnees FACILE...")
        return self.generate_dataset(**self.FACILE)
    
    def generate_moyen(self) -> Tuple[Dict, List[str]]:
        """Génère un jeu de données MOYEN (marge modérée)."""
        print("[MOYEN] Generation d'un jeu de donnees MOYEN...")
        return self.generate_dataset(**self.MOYEN)
    
    def generate_difficile(self) -> Tuple[Dict, List[str]]:
        """Génère un jeu de données DIFFICILE (très peu de marge)."""
        print("[DIFFICILE] Generation d'un jeu de donnees DIFFICILE...")
        return self.generate_dataset(**self.DIFFICILE)
    
    def save_to_csv(
        self,
        tasks: Dict,
        machines: List[str],
        filename: str
    ):
        """
        Sauvegarde le jeu de données dans un fichier CSV.
        
        Args:
            tasks: Dictionnaire des tâches
            machines: Liste des machines
            filename: Nom du fichier CSV de sortie
        """
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['task_name', 'duration', 'successors', 'release_date', 'due_date']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            
            # Écrire les tâches
            for task_name, task_info in tasks.items():
                writer.writerow({
                    'task_name': task_name,
                    'duration': task_info.duration,
                    'successors': task_info.successors,
                    'release_date': task_info.release_date,
                    'due_date': task_info.due_date
                })
            
            # Ligne vide de séparation
            writer.writerow({})
            
            # Informations sur les machines
            writer.writerow({
                'task_name': 'MACHINES',
                'duration': ','.join(machines),
                'successors': '',
                'release_date': '',
                'due_date': ''
            })
        
        print(f"Jeu de donnees sauvegarde dans: {filename}")
    
    def load_from_csv(self, filename: str) -> Tuple[Dict, List[str]]:
        """
        Charge un jeu de données depuis un fichier CSV.
        
        Args:
            filename: Nom du fichier CSV
            
        Returns:
            (dictionnaire_tâches, liste_machines)
        """
        tasks = {}
        machines = []
        
        with open(filename, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            
            for row in reader:
                if row['task_name'] == 'MACHINES':
                    machines = row['duration'].split(',')
                    break
                
                if row['task_name']:  # Ignorer les lignes vides
                    tasks[row['task_name']] = self.taskInfo(
                        duration=int(row['duration']),
                        successors=row['successors'],
                        release_date=int(row['release_date']),
                        due_date=int(row['due_date'])
                    )
        
        print(f"Jeu de donnees charge depuis: {filename}")
        return tasks, machines
    
    def print_stats(self, tasks: Dict, machines: List[str]):
        """
        Affiche les statistiques du jeu de données.
        
        Args:
            tasks: Dictionnaire des tâches
            machines: Liste des machines
        """
        print("\n" + "="*60)
        print("STATISTIQUES DU JEU DE DONNEES")
        print("="*60)
        
        print(f"\nTaches:")
        print(f"   - Nombre total de taches: {len(tasks)}")
        print(f"   - Nombre de projets (paires): {len(tasks) // 2}")
        
        durations = [task.duration for task in tasks.values()]
        print(f"\nDurees:")
        print(f"   - Minimum: {min(durations)} unites")
        print(f"   - Maximum: {max(durations)} unites")
        print(f"   - Moyenne: {sum(durations) / len(durations):.1f} unites")
        
        print(f"\nMachines:")
        print(f"   - Nombre de machines: {len(machines)}")
        print(f"   - Noms: {', '.join(machines)}")
        
        release_dates = [task.release_date for task in tasks.values()]
        due_dates = [task.due_date for task in tasks.values()]
        print(f"\nDates:")
        print(f"   - Dates de disponibilite: {min(release_dates)} - {max(release_dates)}")
        print(f"   - Dates d'echeance: {min(due_dates)} - {max(due_dates)}")
        
        # Calculer la marge moyenne
        slacks = []
        for task_name, task_info in tasks.items():
            slack = task_info.due_date - task_info.release_date - task_info.duration
            slacks.append(slack)
        
        avg_slack = sum(slacks) / len(slacks)
        print(f"\nMarge (Slack):")
        print(f"   - Marge moyenne: {avg_slack:.1f} unites")
        
        num_with_successors = sum(1 for task in tasks.values() if task.successors != "none")
        print(f"\nPrecedences:")
        print(f"   - Taches avec successeur: {num_with_successors}")
        print(f"   - Taches sans successeur: {len(tasks) - num_with_successors}")
        
        print("\n" + "="*60 + "\n")


def main():
    """
    Démonstration du générateur de jeux de données.
    """
    print("\n" + "="*70)
    print(" GENERATEUR DE JEUX DE DONNEES - ORDONNANCEMENT")
    print("="*70 + "\n")
    
    # Créer le générateur (sans seed = génération aléatoire)
    generator = SchedulingDatasetGenerator()
    
    print(f"Graine aleatoire utilisee: {generator.current_seed}\n")
    
    # ============================================
    # NIVEAU 1: FACILE
    # ============================================
    print("\n" + "-"*70)
    tasks_facile, machines_facile = generator.generate_facile()
    generator.print_stats(tasks_facile, machines_facile)
    generator.save_to_csv(tasks_facile, machines_facile, "dataset_facile.csv")
    
    # ============================================
    # NIVEAU 2: MOYEN
    # ============================================
    print("\n" + "-"*70)
    tasks_moyen, machines_moyen = generator.generate_moyen()
    generator.print_stats(tasks_moyen, machines_moyen)
    generator.save_to_csv(tasks_moyen, machines_moyen, "dataset_moyen.csv")
    
    # ============================================
    # NIVEAU 3: DIFFICILE
    # ============================================
    print("\n" + "-"*70)
    tasks_difficile, machines_difficile = generator.generate_difficile()
    generator.print_stats(tasks_difficile, machines_difficile)
    generator.save_to_csv(tasks_difficile, machines_difficile, "dataset_difficile.csv")
    
    print("\n" + "="*70)
    print(" GENERATION TERMINEE AVEC SUCCES")
    print("="*70)
    
    print("\nFichiers generes:")
    print("   - dataset_facile.csv")
    print("   - dataset_moyen.csv")
    print("   - dataset_difficile.csv")
    
    print("\nUtilisation:")
    print("   1. Chargez un fichier CSV dans votre notebook")
    print("   2. Resolvez avec Machine_Parallele")
    print("   3. Analysez les resultats avec print_summary() et visualize_gantt()")
    
    print("\nPour generer de nouveaux jeux de donnees aleatoires:")
    print("   Reexecutez ce script: python generator.py\n")


if __name__ == "__main__":
    main()
