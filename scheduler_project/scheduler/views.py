"""
Views for Task Scheduler Application
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse, FileResponse
from .models import Schedule, Task, Machine, UploadedFile
from .forms import CSVUploadForm, TaskForm, MachineForm, ScheduleNameForm
from .solver import solve_schedule, parse_csv_file
from .pdf_export import generate_pdf_report
import os


def index(request):
    """
    Home page - shows list of schedules
    """
    schedules = Schedule.objects.all()
    return render(request, 'scheduler/index.html', {'schedules': schedules})


def create_schedule_choice(request):
    """
    Choose how to create a schedule (CSV upload or manual entry)
    """
    return render(request, 'scheduler/create_choice.html')


def upload_csv(request):
    """
    Upload CSV file to create a schedule
    """
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Create schedule
            schedule_name = form.cleaned_data.get('schedule_name') or f"Schedule {Schedule.objects.count() + 1}"
            schedule = Schedule.objects.create(name=schedule_name)
            
            # Save uploaded file
            uploaded_file = form.save(commit=False)
            uploaded_file.schedule = schedule
            uploaded_file.save()
            
            # Parse CSV
            file_path = uploaded_file.file.path
            tasks_dict, machines_list = parse_csv_file(file_path)
            
            if tasks_dict is None or machines_list is None:
                messages.error(request, "Error parsing CSV file. Please check the format.")
                schedule.delete()
                return redirect('upload_csv')
            
            # Create machines
            for machine_name in machines_list:
                Machine.objects.create(schedule=schedule, name=machine_name.strip())
            
            # Create tasks
            for task_name, task_data in tasks_dict.items():
                Task.objects.create(
                    schedule=schedule,
                    name=task_name,
                    duration=task_data['duration'],
                    successor_name=task_data['successor_name'],
                    release_date=task_data['release_date'],
                    due_date=task_data['due_date']
                )
            
            messages.success(request, f"CSV uploaded successfully! {len(tasks_dict)} tasks and {len(machines_list)} machines loaded.")
            return redirect('schedule_detail', schedule_id=schedule.id)
    else:
        form = CSVUploadForm()
    
    return render(request, 'scheduler/upload_csv.html', {'form': form})


def manual_entry(request):
    """
    Create schedule manually
    """
    if request.method == 'POST':
        name_form = ScheduleNameForm(request.POST)
        if name_form.is_valid():
            schedule_name = name_form.cleaned_data['name']
            schedule = Schedule.objects.create(name=schedule_name)
            messages.success(request, f"Schedule '{schedule_name}' created. Now add machines and tasks.")
            return redirect('add_machines', schedule_id=schedule.id)
    else:
        name_form = ScheduleNameForm()
    
    return render(request, 'scheduler/manual_entry.html', {'name_form': name_form})


def add_machines(request, schedule_id):
    """
    Add machines to a schedule
    """
    schedule = get_object_or_404(Schedule, id=schedule_id)
    
    if request.method == 'POST':
        if 'add_machine' in request.POST:
            form = MachineForm(request.POST)
            if form.is_valid():
                machine = form.save(commit=False)
                machine.schedule = schedule
                machine.save()
                messages.success(request, f"Machine '{machine.name}' added.")
                return redirect('add_machines', schedule_id=schedule.id)
        
        elif 'done' in request.POST:
            if schedule.machines.count() == 0:
                messages.error(request, "Please add at least one machine.")
            else:
                return redirect('add_tasks', schedule_id=schedule.id)
    
    form = MachineForm()
    machines = schedule.machines.all()
    
    return render(request, 'scheduler/add_machines.html', {
        'schedule': schedule,
        'form': form,
        'machines': machines
    })


def delete_machine(request, schedule_id, machine_id):
    """
    Delete a machine from a schedule
    """
    machine = get_object_or_404(Machine, id=machine_id, schedule_id=schedule_id)
    machine.delete()
    messages.success(request, "Machine deleted.")
    return redirect('add_machines', schedule_id=schedule_id)


def add_tasks(request, schedule_id):
    """
    Add tasks to a schedule
    """
    schedule = get_object_or_404(Schedule, id=schedule_id)
    
    if request.method == 'POST':
        if 'add_task' in request.POST:
            form = TaskForm(request.POST)
            if form.is_valid():
                task = form.save(commit=False)
                task.schedule = schedule
                task.save()
                messages.success(request, f"Task '{task.name}' added.")
                return redirect('add_tasks', schedule_id=schedule.id)
        
        elif 'done' in request.POST:
            if schedule.tasks.count() == 0:
                messages.error(request, "Please add at least one task.")
            else:
                return redirect('schedule_detail', schedule_id=schedule.id)
    
    form = TaskForm()
    tasks = schedule.tasks.all()
    
    return render(request, 'scheduler/add_tasks.html', {
        'schedule': schedule,
        'form': form,
        'tasks': tasks
    })


def delete_task(request, schedule_id, task_id):
    """
    Delete a task from a schedule
    """
    task = get_object_or_404(Task, id=task_id, schedule_id=schedule_id)
    task.delete()
    messages.success(request, "Task deleted.")
    return redirect('add_tasks', schedule_id=schedule_id)


def schedule_detail(request, schedule_id):
    """
    View schedule details
    """
    schedule = get_object_or_404(Schedule, id=schedule_id)
    tasks = schedule.tasks.all()
    machines = schedule.machines.all()
    
    return render(request, 'scheduler/schedule_detail.html', {
        'schedule': schedule,
        'tasks': tasks,
        'machines': machines
    })


def solve(request, schedule_id):
    """
    Solve the scheduling problem
    """
    schedule = get_object_or_404(Schedule, id=schedule_id)
    
    success, message, gantt_chart = solve_schedule(schedule_id)
    
    if success:
        messages.success(request, message)
        return redirect('results', schedule_id=schedule_id)
    else:
        messages.error(request, message)
        return redirect('schedule_detail', schedule_id=schedule_id)


def results(request, schedule_id):
    """
    View scheduling results with Gantt chart
    """
    schedule = get_object_or_404(Schedule, id=schedule_id)
    
    if schedule.status != 'solved':
        messages.warning(request, "This schedule has not been solved yet.")
        return redirect('schedule_detail', schedule_id=schedule_id)
    
    # Re-solve to get the Gantt chart
    success, message, gantt_chart = solve_schedule(schedule_id)
    
    tasks = schedule.tasks.all().order_by('start_time')
    machines = schedule.machines.all()
    
    # Group tasks by machine
    machine_assignments = {}
    for machine in machines:
        machine_assignments[machine.name] = tasks.filter(assigned_machine=machine).order_by('start_time')
    
    return render(request, 'scheduler/results.html', {
        'schedule': schedule,
        'tasks': tasks,
        'machines': machines,
        'machine_assignments': machine_assignments,
        'gantt_chart': gantt_chart
    })


def export_pdf(request, schedule_id):
    """
    Export schedule results as PDF
    """
    schedule = get_object_or_404(Schedule, id=schedule_id)
    
    if schedule.status != 'solved':
        messages.error(request, "Cannot export unsolved schedule.")
        return redirect('schedule_detail', schedule_id=schedule_id)
    
    # Generate Gantt chart
    success, message, gantt_chart = solve_schedule(schedule_id)
    
    # Generate PDF
    pdf_buffer = generate_pdf_report(schedule, gantt_chart)
    
    response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="schedule_{schedule.id}_{schedule.name}.pdf"'
    
    return response


def delete_schedule(request, schedule_id):
    """
    Delete a schedule
    """
    schedule = get_object_or_404(Schedule, id=schedule_id)
    schedule.delete()
    messages.success(request, "Schedule deleted.")
    return redirect('index')
