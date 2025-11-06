"""
Formulaires pour le planificateur de tâches
"""
from django import forms
from .models import Task, Machine, UploadedFile


class CSVUploadForm(forms.ModelForm):
    """
    Formulaire pour télécharger des fichiers CSV
    """
    schedule_name = forms.CharField(
        max_length=200, 
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Entrez le nom du planning (optionnel)'
        })
    )
    
    class Meta:
        model = UploadedFile
        fields = ['file']
        widgets = {
            'file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.csv'
            })
        }


class MachineForm(forms.ModelForm):
    """
    Formulaire pour ajouter des machines manuellement
    """
    class Meta:
        model = Machine
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ex: m_1, Machine A'
            })
        }


class TaskForm(forms.ModelForm):
    """
    Formulaire pour ajouter des tâches manuellement
    """
    class Meta:
        model = Task
        fields = ['name', 'duration', 'successor_name', 'release_date', 'due_date']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ex: task_a_1'
            }),
            'duration': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'placeholder': 'Durée de la tâche'
            }),
            'successor_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'none ou nom de la tâche successeur'
            }),
            'release_date': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'value': '0',
                'placeholder': 'Date de disponibilité'
            }),
            'due_date': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'placeholder': "Date d'échéance"
            }),
        }
    
    def clean_successor_name(self):
        """Nettoie et valide le nom du successeur"""
        successor = self.cleaned_data.get('successor_name', '').strip()
        return successor if successor else 'none'


class ScheduleNameForm(forms.Form):
    """
    Formulaire simple pour nommer un planning
    """
    name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Entrez le nom du planning'
        })
    )
