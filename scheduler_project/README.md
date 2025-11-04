# Task Scheduler Web Application

A professional Django web application for parallel machine scheduling optimization using Google OR-Tools CP-SAT solver.

## 🎯 Features

- **CSV Import**: Upload CSV files with task and machine data
- **Manual Entry**: Add tasks and machines through interactive forms
- **Solver Integration**: Solve scheduling problems using OR-Tools CP-SAT
- **Gantt Chart Visualization**: Visual timeline of task execution
- **PDF Export**: Generate comprehensive PDF reports with charts
- **Responsive UI**: Modern Bootstrap 5 interface
- **Real-time Statistics**: View makespan, utilization, and critical tasks

## 📁 Project Structure

```
scheduler_project/
├── config/                 # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── scheduler/             # Main application
│   ├── models.py          # Database models
│   ├── views.py           # View controllers
│   ├── forms.py           # Form definitions
│   ├── solver.py          # OR-Tools solver integration
│   ├── pdf_export.py      # PDF generation
│   ├── urls.py            # URL routes
│   ├── admin.py           # Admin configuration
│   └── templates/         # HTML templates
│       └── scheduler/
├── media/                 # Uploaded files
├── manage.py              # Django management script
└── requirements.txt       # Python dependencies
```

## 🚀 Installation & Setup

### Step 1: Install Dependencies

```powershell
# Navigate to project directory
cd "c:\Users\oussa\Desktop\Projet tut\scheduler_project"

# Install required packages
pip install -r requirements.txt
```

### Step 2: Initialize Database

```powershell
# Create database tables
python manage.py makemigrations
python manage.py migrate
```

### Step 3: Create Admin User (Optional)

```powershell
python manage.py createsuperuser
```

### Step 4: Run Development Server

```powershell
python manage.py runserver
```

The application will be available at: **http://127.0.0.1:8000/**

## 📖 Usage Guide

### 1. Create a Schedule

**Option A: Upload CSV File**
- Click "Create New Schedule" → "Upload CSV File"
- Select your CSV file (see format below)
- The system will automatically import tasks and machines

**Option B: Manual Entry**
- Click "Create New Schedule" → "Manual Entry"
- Enter schedule name
- Add machines one by one
- Add tasks with their parameters

### 2. CSV File Format

Your CSV should follow this structure:

```csv
task_name,duration,successors,release_date,due_date
task_a_1,120,task_a_2,0,600
task_a_2,20,none,0,600
task_b_1,120,task_b_2,0,600
task_b_2,120,none,0,600

MACHINES,"m_a,m_b",,,
```

**Important:**
- Header row must include: `task_name,duration,successors,release_date,due_date`
- Use `none` for tasks without successors
- Machines line: `MACHINES,"machine1,machine2,machine3",,,`
- Leave a blank line before the MACHINES row

### 3. Solve the Schedule

- Open your schedule
- Click "Solve Schedule"
- The solver will compute optimal task assignments
- View results with Gantt chart

### 4. Export Results

- From the results page, click "Export as PDF"
- Download a comprehensive report including:
  - Schedule summary
  - Machine assignments
  - Task details table
  - Gantt chart visualization

## 🔧 Configuration

### Database
The project uses SQLite by default. To use PostgreSQL or MySQL, edit `config/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'scheduler_db',
        'USER': 'your_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Static Files
For production deployment:

```powershell
python manage.py collectstatic
```

## 📊 Understanding Results

### Makespan
Total project completion time (maximum end time across all tasks)

### Objective Value
Sum of all task start times (minimized by the solver)

### Slack
Time buffer between task completion and due date
- **Green badge (>5)**: Comfortable margin
- **Red badge (≤5)**: Critical task, little room for delay

### Machine Utilization
Percentage of time each machine is actively working

## 🎨 Customization

### Change Color Scheme
Edit `scheduler/templates/scheduler/base.html`:

```css
:root {
    --primary-color: #2c3e50;    /* Dark blue */
    --secondary-color: #3498db;  /* Light blue */
    --success-color: #2ecc71;    /* Green */
}
```

### Modify Gantt Chart
Edit `scheduler/solver.py` → `Machine_Parallele.generate_gantt_chart()`

## 🐛 Troubleshooting

### No Solution Found
- Increase number of machines
- Relax due dates (increase slack)
- Check for circular dependencies in task successors
- Verify release_date + duration ≤ due_date for all tasks

### CSV Upload Errors
- Ensure UTF-8 encoding
- Check for proper comma separation
- Verify MACHINES line format
- Remove any extra blank lines

### Django Errors
```powershell
# Clear cache and restart
python manage.py flush
python manage.py migrate
python manage.py runserver
```

## 📚 API Reference

### Models

**Schedule**
- `name`: Schedule identifier
- `status`: pending | solved | no_solution | error
- `makespan`: Total completion time
- `objective_value`: Optimization metric

**Machine**
- `name`: Machine identifier
- `schedule`: ForeignKey to Schedule

**Task**
- `name`: Task identifier
- `duration`: Execution time
- `successor_name`: Dependent task
- `release_date`: Earliest start time
- `due_date`: Latest completion time
- `assigned_machine`: Assigned machine (after solving)
- `start_time`: Computed start time
- `end_time`: Computed end time
- `slack`: Time buffer to due date

## 🔒 Security Notes

**For Production:**

1. Change `SECRET_KEY` in `settings.py`
2. Set `DEBUG = False`
3. Configure `ALLOWED_HOSTS`
4. Use environment variables for sensitive data
5. Enable HTTPS
6. Set up proper database authentication

## 📝 Sample CSV Files

The original project includes:
- `dataset_facile.csv` - Easy problem (high slack)
- `dataset_moyen.csv` - Medium problem
- `dataset_difficile.csv` - Hard problem (tight constraints)

Copy these to `scheduler_project/media/samples/` for quick testing.

## 🤝 Contributing

To extend the application:

1. **Add new solver constraints**: Edit `scheduler/solver.py`
2. **Custom visualizations**: Modify `generate_gantt_chart()`
3. **Additional exports**: Create new functions in `pdf_export.py`
4. **New views**: Add to `scheduler/views.py` and `urls.py`

## 📧 Support

For issues or questions:
1. Check the troubleshooting section
2. Review Django documentation: https://docs.djangoproject.com/
3. OR-Tools guide: https://developers.google.com/optimization

## 📄 License

This project is for educational and commercial use.

---

**Happy Scheduling! 🎉**
