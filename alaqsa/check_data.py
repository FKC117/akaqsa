#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alaqsa.settings')
django.setup()

from student.models import Attendance, Class, Student
from datetime import datetime

print("=== DATA CHECK ===")
print(f"Classes: {[(c.id, c.name, c.section) for c in Class.objects.all()]}")
print(f"Students: {Student.objects.count()}")
print(f"Total Attendance records: {Attendance.objects.count()}")

if Attendance.objects.exists():
    print("\n=== SAMPLE ATTENDANCE DATA ===")
    for att in Attendance.objects.all()[:5]:
        print(f"ID: {att.id}, Student: {att.student.full_name}, Class: {att.student.current_class}, Date: {att.date}, Present: {att.is_present}, Reason: {att.reason}")
    
    print("\n=== DATE RANGE CHECK ===")
    start_date = datetime(2025, 7, 10).date()
    end_date = datetime(2025, 7, 13).date()
    class_id = 1
    
    filtered = Attendance.objects.filter(
        date__gte=start_date,
        date__lte=end_date,
        student__current_class__id=class_id
    )
    
    print(f"Filtered records for date range {start_date} to {end_date} and class_id {class_id}: {filtered.count()}")
    
    if filtered.exists():
        for att in filtered:
            print(f"  - {att.student.full_name} on {att.date}: {'Present' if att.is_present else 'Absent'}")
    else:
        print("  No records found!")
        
        # Check what dates exist
        dates = Attendance.objects.values_list('date', flat=True).distinct().order_by('date')
        print(f"Available dates: {list(dates)}")
        
        # Check what classes exist in attendance
        classes = Attendance.objects.values_list('student__current_class__id', 'student__current_class__name', 'student__current_class__section').distinct()
        print(f"Classes in attendance: {list(classes)}")
else:
    print("No attendance records found!") 