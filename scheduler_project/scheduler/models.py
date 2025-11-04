"""
Database Models for Task Scheduler
"""
from django.db import models
from django.utils import timezone


class Schedule(models.Model):
    """
    Represents a scheduling session/project
    """
    name = models.CharField(max_length=200, default="Schedule")
    created_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('solved', 'Solved'),
            ('no_solution', 'No Solution'),
            ('error', 'Error')
        ],
        default='pending'
    )
    makespan = models.IntegerField(null=True, blank=True)
    objective_value = models.FloatField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"


class Machine(models.Model):
    """
    Represents a machine
    """
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name='machines')
    name = models.CharField(max_length=100)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Task(models.Model):
    """
    Represents a task to be scheduled
    """
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name='tasks')
    name = models.CharField(max_length=100)
    duration = models.IntegerField()
    successor_name = models.CharField(max_length=100, blank=True, default='none')
    release_date = models.IntegerField(default=0)
    due_date = models.IntegerField()
    
    # Solution fields (filled after solving)
    assigned_machine = models.ForeignKey(
        Machine, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='assigned_tasks'
    )
    start_time = models.IntegerField(null=True, blank=True)
    end_time = models.IntegerField(null=True, blank=True)
    slack = models.IntegerField(null=True, blank=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} (Duration: {self.duration})"


class UploadedFile(models.Model):
    """
    Stores uploaded CSV files
    """
    schedule = models.OneToOneField(Schedule, on_delete=models.CASCADE, related_name='uploaded_file')
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"File for {self.schedule.name}"
