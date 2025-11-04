"""
Django Admin Configuration for Scheduler App
"""
from django.contrib import admin
from .models import Schedule, Machine, Task, UploadedFile


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at', 'status', 'makespan', 'objective_value']
    list_filter = ['status', 'created_at']
    search_fields = ['name']
    readonly_fields = ['created_at']


@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    list_display = ['name', 'schedule']
    list_filter = ['schedule']
    search_fields = ['name']


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['name', 'schedule', 'duration', 'assigned_machine', 'start_time', 'end_time']
    list_filter = ['schedule', 'assigned_machine']
    search_fields = ['name']


@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ['schedule', 'uploaded_at']
    list_filter = ['uploaded_at']
