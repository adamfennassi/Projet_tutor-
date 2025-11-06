"""
Modèles de base de données pour le planificateur de tâches
"""
from django.db import models
from django.utils import timezone


class Schedule(models.Model):
    """
    Représente une session d'ordonnancement / un projet
    """
    name = models.CharField(max_length=200, default="Schedule")
    created_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'En attente'),
            ('solved', 'Résolu'),
            ('no_solution', 'Aucune solution'),
            ('error', 'Erreur')
        ],
        default='pending'
    )
    makespan = models.IntegerField(null=True, blank=True)  # Durée totale du projet
    objective_value = models.FloatField(null=True, blank=True)  # Valeur de la fonction objectif
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"


class Machine(models.Model):
    """
    Représente une machine
    """
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name='machines')
    name = models.CharField(max_length=100)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Task(models.Model):
    """
    Représente une tâche à ordonnancer
    """
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name='tasks')
    name = models.CharField(max_length=100)
    duration = models.IntegerField()  # Durée d'exécution
    successor_name = models.CharField(max_length=100, blank=True, default='none')  # Nom du successeur
    release_date = models.IntegerField(default=0)  # Date de disponibilité
    due_date = models.IntegerField()  # Date d'échéance
    
    # Champs de solution (remplis après résolution)
    assigned_machine = models.ForeignKey(
        Machine, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='assigned_tasks'
    )
    start_time = models.IntegerField(null=True, blank=True)  # Date de début calculée
    end_time = models.IntegerField(null=True, blank=True)  # Date de fin calculée
    slack = models.IntegerField(null=True, blank=True)  # Marge avant l'échéance
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} (Durée: {self.duration})"


class UploadedFile(models.Model):
    """
    Stocke les fichiers CSV téléchargés
    """
    schedule = models.OneToOneField(Schedule, on_delete=models.CASCADE, related_name='uploaded_file')
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Fichier pour {self.schedule.name}"
