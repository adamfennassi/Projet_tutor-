# QUICK REFERENCE GUIDE

## 🚀 Getting Started (30 seconds)

```powershell
cd "c:\Users\oussa\Desktop\Projet tut\scheduler_project"
.\setup.ps1
```

Then open: http://127.0.0.1:8000/

## 📋 Common Commands

### Start Server
```powershell
python manage.py runserver
```

### Create Admin User
```powershell
python manage.py createsuperuser
```

### Reset Database
```powershell
del db.sqlite3
python manage.py migrate
```

### Run Migrations
```powershell
python manage.py makemigrations
python manage.py migrate
```

## 🎯 User Workflows

### Workflow 1: CSV Upload (Fastest)
1. Home → "Create New Schedule"
2. "Upload CSV File"
3. Select CSV → Upload
4. "Solve Schedule"
5. View Results → Export PDF

**Time: ~2 minutes**

### Workflow 2: Manual Entry
1. Home → "Create New Schedule"
2. "Manual Entry"
3. Enter name → Continue
4. Add machines (click "Add Machine" for each)
5. "Done - Add Tasks"
6. Add tasks (fill form for each)
7. "Done - View Schedule"
8. "Solve Schedule"
9. View Results → Export PDF

**Time: ~5 minutes**

## 📊 CSV Format Cheat Sheet

```csv
task_name,duration,successors,release_date,due_date
task_a_1,120,task_a_2,0,600
task_a_2,20,none,0,600

MACHINES,"m_1,m_2",,,
```

**Rules:**
- ✓ Header row required
- ✓ `none` for no successor
- ✓ Blank line before MACHINES
- ✓ Machines in quotes, comma-separated

## 🎨 Key Features by Page

### Home Page
- View all schedules
- Quick status overview
- Direct access to results

### Schedule Detail
- View tasks and machines
- Solve button
- Statistics summary

### Results Page
- Gantt chart visualization
- Machine assignments
- Task execution timeline
- PDF export button

## 🔍 Status Badges

| Badge | Meaning |
|-------|---------|
| 🟢 Solved | Schedule successfully optimized |
| 🟡 Pending | Not yet solved |
| 🔴 No Solution | Constraints too tight |
| ⚫ Error | Technical issue |

## ⚙️ Solver Parameters

Edit `scheduler/solver.py` to customize:

```python
# Objective: Minimize sum of start times
self.model.Minimize(
    sum(self.start_time_vars[task_name] for task_name in self.tasks)
)
```

**Alternative objectives:**
- Minimize makespan
- Minimize tardiness
- Balance machine loads

## 📈 Understanding Results

### Makespan
Total project duration = latest task end time

### Objective Value
Sum of all start times (lower is better)

### Slack
Buffer time before deadline
- **Green (>5)**: Safe
- **Red (≤5)**: Critical

### Utilization
```
Utilization = (Total Work Time / Makespan) × 100%
```

## 🎯 Tips for Better Solutions

### No Solution Found?
1. ✅ Add more machines
2. ✅ Extend due dates
3. ✅ Reduce task durations
4. ✅ Check successor relationships
5. ✅ Verify: `release_date + duration ≤ due_date`

### Improve Makespan
1. Balance task distribution
2. Minimize dependencies
3. Use more machines
4. Parallel task execution

### Reduce Critical Tasks
1. Increase slack factor
2. Earlier release dates
3. Later due dates

## 🛠️ Customization Quick Edits

### Change Theme Colors
`scheduler/templates/scheduler/base.html`:
```css
:root {
    --primary-color: #2c3e50;
    --secondary-color: #3498db;
}
```

### Modify Gantt Chart Size
`scheduler/solver.py`:
```python
fig, ax = plt.subplots(figsize=(14, 6))  # width, height
```

### Adjust Critical Slack Threshold
`scheduler/solver.py`:
```python
if info['slack'] <= 5:  # Change this value
```

## 📱 Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| Stop Server | Ctrl + C |
| Refresh Page | F5 |
| Open DevTools | F12 |

## 🐛 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| Can't access site | Check if server is running |
| No solution | Add machines / relax deadlines |
| CSV error | Check format / encoding (UTF-8) |
| Blank page | Check browser console (F12) |
| Changes not showing | Hard refresh (Ctrl + F5) |

## 📞 File Locations

```
Key Files:
├── Models: scheduler/models.py
├── Solver: scheduler/solver.py
├── Views: scheduler/views.py
├── Templates: scheduler/templates/scheduler/
├── Database: db.sqlite3
└── Uploads: media/uploads/
```

## 🎓 Learning Path

1. **Beginner**: Use CSV upload with sample files
2. **Intermediate**: Manual entry, understand constraints
3. **Advanced**: Customize solver, modify objectives
4. **Expert**: Add new features, integrate ML

## 💾 Backup & Export

### Export Database
```powershell
copy db.sqlite3 backup_$(Get-Date -Format 'yyyyMMdd').sqlite3
```

### Export All Schedules as PDF
Use the "Export PDF" button on each results page

### Bulk Operations
Use Django admin panel: http://127.0.0.1:8000/admin/

## 📊 Performance Benchmarks

| Dataset | Tasks | Machines | Solve Time |
|---------|-------|----------|------------|
| Easy | 6 | 4 | <1 sec |
| Medium | 10 | 3 | 1-2 sec |
| Hard | 16 | 2 | 2-5 sec |
| Very Hard | 30+ | 5+ | 5-30 sec |

## 🔐 Security Checklist

For production deployment:

- [ ] `DEBUG = False`
- [ ] Change `SECRET_KEY`
- [ ] Set `ALLOWED_HOSTS`
- [ ] Use HTTPS
- [ ] Enable CSRF protection
- [ ] Validate file uploads
- [ ] Rate limiting
- [ ] Regular backups

## 📚 Resources

- **Django Docs**: https://docs.djangoproject.com/
- **OR-Tools**: https://developers.google.com/optimization
- **Bootstrap 5**: https://getbootstrap.com/docs/5.3/
- **ReportLab**: https://www.reportlab.com/docs/

---

**Need Help?** Check SETUP.md and README.md for detailed documentation.
