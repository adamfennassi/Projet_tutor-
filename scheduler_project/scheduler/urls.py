"""
Configuration des URLs pour l'application Scheduler
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create_schedule_choice, name='create_choice'),
    path('upload/', views.upload_csv, name='upload_csv'),
    path('manual/', views.manual_entry, name='manual_entry'),
    path('schedule/<int:schedule_id>/', views.schedule_detail, name='schedule_detail'),
    path('schedule/<int:schedule_id>/add-machines/', views.add_machines, name='add_machines'),
    path('schedule/<int:schedule_id>/add-tasks/', views.add_tasks, name='add_tasks'),
    path('schedule/<int:schedule_id>/machine/<int:machine_id>/delete/', views.delete_machine, name='delete_machine'),
    path('schedule/<int:schedule_id>/task/<int:task_id>/delete/', views.delete_task, name='delete_task'),
    path('schedule/<int:schedule_id>/solve/', views.solve, name='solve'),
    path('schedule/<int:schedule_id>/results/', views.results, name='results'),
    path('schedule/<int:schedule_id>/export-pdf/', views.export_pdf, name='export_pdf'),
    path('schedule/<int:schedule_id>/delete/', views.delete_schedule, name='delete_schedule'),
]
