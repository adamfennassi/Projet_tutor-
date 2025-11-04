# SETUP INSTRUCTIONS

## Quick Start Guide

### 1. Navigate to Project Directory
```powershell
cd "c:\Users\oussa\Desktop\Projet tut\scheduler_project"
```

### 2. Install Dependencies
```powershell
pip install -r requirements.txt
```

**Expected packages:**
- Django 4.2+
- ortools 9.7+
- matplotlib 3.7+
- pandas 2.0+
- reportlab 4.0+
- Pillow 10.0+

### 3. Initialize Database
```powershell
python manage.py makemigrations scheduler
python manage.py migrate
```

### 4. (Optional) Create Admin User
```powershell
python manage.py createsuperuser
```
Follow prompts to create username and password.

### 5. Copy Sample Datasets
Copy the sample CSV files to the media folder:
```powershell
# Create samples directory
mkdir media\samples

# Copy existing datasets
copy "..\dataset_facile.csv" "media\samples\"
copy "..\dataset_moyen.csv" "media\samples\"
copy "..\dataset_difficile.csv" "media\samples\"
```

### 6. Run Development Server
```powershell
python manage.py runserver
```

### 7. Access Application
Open your browser and navigate to:
- **Main app**: http://127.0.0.1:8000/
- **Admin panel**: http://127.0.0.1:8000/admin/

## First Time Usage

### Test with CSV Upload
1. Go to http://127.0.0.1:8000/
2. Click "Create New Schedule"
3. Choose "Upload CSV File"
4. Select `dataset_facile.csv` from `media/samples/`
5. Click "Upload and Process"
6. Click "Solve Schedule"
7. View results and Gantt chart
8. Export as PDF

### Test with Manual Entry
1. Click "Create New Schedule"
2. Choose "Manual Entry"
3. Enter schedule name: "Test Schedule"
4. Add machines:
   - m_1
   - m_2
5. Add tasks:
   - Task: task_a, Duration: 50, Successor: none, Release: 0, Due: 200
   - Task: task_b, Duration: 60, Successor: none, Release: 0, Due: 200
6. Click "Done - View Schedule"
7. Click "Solve Schedule"
8. View results

## Project Structure Overview

```
scheduler_project/
├── config/                      # Django settings
│   ├── __init__.py
│   ├── settings.py             # Main configuration
│   ├── urls.py                 # Root URL routing
│   └── wsgi.py                 # WSGI application
│
├── scheduler/                   # Main app
│   ├── __init__.py
│   ├── admin.py                # Admin panel config
│   ├── apps.py                 # App configuration
│   ├── forms.py                # Form definitions
│   ├── models.py               # Database models
│   ├── pdf_export.py           # PDF generation
│   ├── solver.py               # OR-Tools integration
│   ├── urls.py                 # App URL routing
│   ├── views.py                # View controllers
│   ├── templates/
│   │   └── scheduler/
│   │       ├── base.html       # Base template
│   │       ├── index.html      # Home page
│   │       ├── create_choice.html
│   │       ├── upload_csv.html
│   │       ├── manual_entry.html
│   │       ├── add_machines.html
│   │       ├── add_tasks.html
│   │       ├── schedule_detail.html
│   │       └── results.html
│   └── static/
│       └── scheduler/
│
├── media/                      # User uploads
│   ├── uploads/               # Uploaded CSV files
│   └── samples/               # Sample datasets
│
├── db.sqlite3                 # SQLite database
├── manage.py                  # Django CLI
├── requirements.txt           # Python dependencies
└── README.md                  # Full documentation
```

## Database Schema

### Schedule
- id (AutoField)
- name (CharField)
- created_at (DateTimeField)
- status (CharField): pending/solved/no_solution/error
- makespan (IntegerField, nullable)
- objective_value (FloatField, nullable)

### Machine
- id (AutoField)
- schedule (ForeignKey → Schedule)
- name (CharField)

### Task
- id (AutoField)
- schedule (ForeignKey → Schedule)
- name (CharField)
- duration (IntegerField)
- successor_name (CharField)
- release_date (IntegerField)
- due_date (IntegerField)
- assigned_machine (ForeignKey → Machine, nullable)
- start_time (IntegerField, nullable)
- end_time (IntegerField, nullable)
- slack (IntegerField, nullable)

### UploadedFile
- id (AutoField)
- schedule (OneToOneField → Schedule)
- file (FileField)
- uploaded_at (DateTimeField)

## URLs Reference

| URL | View | Description |
|-----|------|-------------|
| / | index | Home page with schedule list |
| /create/ | create_choice | Choose CSV or manual entry |
| /upload/ | upload_csv | CSV upload form |
| /manual/ | manual_entry | Manual schedule creation |
| /schedule/<id>/ | schedule_detail | View schedule details |
| /schedule/<id>/add-machines/ | add_machines | Add machines to schedule |
| /schedule/<id>/add-tasks/ | add_tasks | Add tasks to schedule |
| /schedule/<id>/solve/ | solve | Run solver |
| /schedule/<id>/results/ | results | View results with Gantt |
| /schedule/<id>/export-pdf/ | export_pdf | Download PDF report |
| /schedule/<id>/delete/ | delete_schedule | Delete schedule |

## Troubleshooting Common Issues

### Issue: "No module named 'django'"
**Solution:**
```powershell
pip install Django
```

### Issue: "No module named 'ortools'"
**Solution:**
```powershell
pip install ortools
```

### Issue: Django can't find templates
**Solution:**
Ensure `APP_DIRS: True` in `config/settings.py` TEMPLATES configuration.

### Issue: Static files not loading
**Solution:**
```powershell
python manage.py collectstatic
```

### Issue: "CSRF verification failed"
**Solution:**
Ensure `{% csrf_token %}` is in all forms and cookies are enabled.

### Issue: No solution found for schedule
**Solutions:**
- Add more machines
- Increase due dates
- Reduce task durations
- Check for circular dependencies in successors

## Development Tips

### Reset Database
```powershell
del db.sqlite3
python manage.py migrate
```

### View Database
Use DB Browser for SQLite: https://sqlitebrowser.org/

### Debug Mode
Set `DEBUG = True` in `config/settings.py` to see detailed errors.

### Check Logs
Django prints errors to console where `runserver` is running.

## Production Deployment Checklist

- [ ] Set `DEBUG = False`
- [ ] Change `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set up PostgreSQL/MySQL
- [ ] Configure static files serving
- [ ] Enable HTTPS
- [ ] Set up gunicorn/uwsgi
- [ ] Configure nginx/Apache
- [ ] Set up backup system
- [ ] Enable logging
- [ ] Configure email backend
- [ ] Set up monitoring

## Next Steps

1. **Test the application** with sample datasets
2. **Customize the UI** in templates
3. **Adjust solver parameters** in `solver.py`
4. **Add authentication** for multi-user support
5. **Deploy to production** server

---

For detailed documentation, see README.md
