"""
Forms for Task Scheduler
"""
from django import forms
from .models import Task, Machine, UploadedFile


class CSVUploadForm(forms.ModelForm):
    """
    Form for uploading CSV files
    """
    schedule_name = forms.CharField(
        max_length=200, 
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter schedule name (optional)'
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
    Form for adding machines manually
    """
    class Meta:
        model = Machine
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., m_1, Machine A'
            })
        }


class TaskForm(forms.ModelForm):
    """
    Form for adding tasks manually
    """
    class Meta:
        model = Task
        fields = ['name', 'duration', 'successor_name', 'release_date', 'due_date']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., task_a_1'
            }),
            'duration': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'placeholder': 'Task duration'
            }),
            'successor_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'none or successor task name'
            }),
            'release_date': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'value': '0',
                'placeholder': 'Release date'
            }),
            'due_date': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'placeholder': 'Due date'
            }),
        }
    
    def clean_successor_name(self):
        successor = self.cleaned_data.get('successor_name', '').strip()
        return successor if successor else 'none'


class ScheduleNameForm(forms.Form):
    """
    Simple form for naming a schedule
    """
    name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter schedule name'
        })
    )
