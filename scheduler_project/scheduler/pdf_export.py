"""
PDF Export Module - Generates PDF reports for schedules
"""
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import io
import base64
from datetime import datetime


def generate_pdf_report(schedule, gantt_chart_base64):
    """
    Generate a PDF report for a schedule
    
    Args:
        schedule: Schedule model instance
        gantt_chart_base64: Base64 encoded Gantt chart image
        
    Returns:
        io.BytesIO: PDF file buffer
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.75*inch, bottomMargin=0.75*inch)
    
    # Container for PDF elements
    elements = []
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#34495e'),
        spaceAfter=12,
        spaceBefore=12
    )
    
    # Title
    title = Paragraph(f"<b>Schedule Report: {schedule.name}</b>", title_style)
    elements.append(title)
    elements.append(Spacer(1, 0.2*inch))
    
    # Summary Information
    summary_heading = Paragraph("<b>Summary</b>", heading_style)
    elements.append(summary_heading)
    
    summary_data = [
        ['Schedule Name:', schedule.name],
        ['Created:', schedule.created_at.strftime('%Y-%m-%d %H:%M')],
        ['Status:', schedule.get_status_display()],
        ['Makespan:', f"{schedule.makespan} time units" if schedule.makespan else 'N/A'],
        ['Objective Value:', f"{schedule.objective_value:.2f}" if schedule.objective_value else 'N/A'],
        ['Number of Tasks:', str(schedule.tasks.count())],
        ['Number of Machines:', str(schedule.machines.count())],
    ]
    
    summary_table = Table(summary_data, colWidths=[2*inch, 4*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ecf0f1')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    
    elements.append(summary_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Machine Assignments
    machines_heading = Paragraph("<b>Machine Assignments</b>", heading_style)
    elements.append(machines_heading)
    
    machine_data = [['Machine', 'Assigned Tasks', 'Utilization']]
    
    for machine in schedule.machines.all():
        assigned_tasks = machine.assigned_tasks.all()
        task_names = ', '.join([task.name for task in assigned_tasks])
        total_work = sum([task.duration for task in assigned_tasks])
        utilization = f"{(total_work / schedule.makespan * 100):.1f}%" if schedule.makespan else 'N/A'
        
        machine_data.append([
            machine.name,
            task_names if task_names else 'None',
            utilization
        ])
    
    machine_table = Table(machine_data, colWidths=[1.5*inch, 3.5*inch, 1.5*inch])
    machine_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#ecf0f1')]),
    ]))
    
    elements.append(machine_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Task Details
    tasks_heading = Paragraph("<b>Task Details</b>", heading_style)
    elements.append(tasks_heading)
    
    task_data = [['Task', 'Duration', 'Start', 'End', 'Machine', 'Slack']]
    
    for task in schedule.tasks.all().order_by('start_time'):
        task_data.append([
            task.name,
            str(task.duration),
            str(task.start_time) if task.start_time is not None else 'N/A',
            str(task.end_time) if task.end_time is not None else 'N/A',
            task.assigned_machine.name if task.assigned_machine else 'N/A',
            str(task.slack) if task.slack is not None else 'N/A',
        ])
    
    task_table = Table(task_data, colWidths=[1.3*inch, 0.9*inch, 0.9*inch, 0.9*inch, 1.3*inch, 0.9*inch])
    task_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2ecc71')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#ecf0f1')]),
    ]))
    
    elements.append(task_table)
    
    # Add page break before Gantt chart
    elements.append(PageBreak())
    
    # Gantt Chart
    if gantt_chart_base64:
        gantt_heading = Paragraph("<b>Gantt Chart</b>", heading_style)
        elements.append(gantt_heading)
        elements.append(Spacer(1, 0.2*inch))
        
        # Decode base64 image
        image_data = base64.b64decode(gantt_chart_base64)
        image_buffer = io.BytesIO(image_data)
        
        # Add image to PDF
        img = Image(image_buffer, width=6.5*inch, height=4*inch)
        elements.append(img)
    
    # Footer
    elements.append(Spacer(1, 0.5*inch))
    footer_text = f"<i>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</i>"
    footer = Paragraph(footer_text, styles['Normal'])
    elements.append(footer)
    
    # Build PDF
    doc.build(elements)
    
    buffer.seek(0)
    return buffer
