from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Class, Subject, Student, Attendance, ClassRoutine, Exam, 
    Result, FeeCategory, Fee, Notice, StudentDocument, StudentPerformance
)


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ['name', 'section', 'capacity', 'total_students', 'created_at']
    list_filter = ['name', 'section']
    search_fields = ['name', 'section']
    ordering = ['name', 'section']


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'code', 'description']
    ordering = ['name']


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = [
        'student_id', 'full_name', 'current_class', 'roll_number', 
        'gender', 'age', 'is_active', 'admission_date'
    ]
    list_filter = [
        'current_class', 'gender', 'is_active', 'admission_date', 
        'blood_group', 'city'
    ]
    search_fields = [
        'first_name', 'last_name', 'student_id', 'roll_number', 
        'email', 'phone', 'father_name', 'mother_name'
    ]
    readonly_fields = ['student_id', 'created_at', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('student_id', 'first_name', 'last_name', 'date_of_birth', 
                      'gender', 'blood_group', 'photo')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone', 'address', 'city', 'state', 'postal_code')
        }),
        ('Academic Information', {
            'fields': ('current_class', 'admission_date', 'roll_number')
        }),
        ('Parent/Guardian Information', {
            'fields': ('father_name', 'mother_name', 'parent_phone', 'parent_email')
        }),
        ('Emergency Contact', {
            'fields': ('emergency_contact_name', 'emergency_contact_phone', 
                      'emergency_contact_relation')
        }),
        ('Medical Information', {
            'fields': ('medical_conditions', 'allergies')
        }),
        ('Documents', {
            'fields': ('birth_certificate',)
        }),
        ('Status', {
            'fields': ('is_active', 'created_at', 'updated_at')
        }),
    )
    ordering = ['current_class', 'roll_number']


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['student', 'date', 'is_present', 'reason', 'created_at']
    list_filter = ['is_present', 'date', 'student__current_class']
    search_fields = ['student__first_name', 'student__last_name', 'student__roll_number']
    date_hierarchy = 'date'
    ordering = ['-date', 'student']


@admin.register(ClassRoutine)
class ClassRoutineAdmin(admin.ModelAdmin):
    list_display = ['class_name', 'subject', 'day', 'start_time', 'end_time', 'room_number', 'teacher_name']
    list_filter = ['class_name', 'subject', 'day']
    search_fields = ['class_name__name', 'subject__name', 'teacher_name']
    ordering = ['class_name', 'day', 'start_time']


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ['name', 'exam_type', 'subject', 'class_name', 'exam_date', 'total_marks', 'pass_marks']
    list_filter = ['exam_type', 'subject', 'class_name', 'exam_date']
    search_fields = ['name', 'subject__name', 'class_name__name']
    date_hierarchy = 'exam_date'
    ordering = ['-exam_date', 'class_name']


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = [
        'student', 'exam', 'marks_obtained', 'percentage', 'grade', 
        'is_pass', 'created_at'
    ]
    list_filter = [
        'exam__exam_type', 'exam__subject', 'exam__class_name', 
        'created_at'
    ]
    search_fields = [
        'student__first_name', 'student__last_name', 'student__roll_number',
        'exam__name'
    ]
    readonly_fields = ['percentage', 'grade', 'is_pass']
    ordering = ['-created_at']


@admin.register(FeeCategory)
class FeeCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'amount', 'is_monthly', 'created_at']
    list_filter = ['is_monthly', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['name']


@admin.register(Fee)
class FeeAdmin(admin.ModelAdmin):
    list_display = [
        'student', 'fee_category', 'amount', 'paid_amount', 'remaining_amount',
        'payment_status', 'due_date', 'is_overdue'
    ]
    list_filter = [
        'payment_status', 'payment_method', 'fee_category', 
        'student__current_class', 'due_date'
    ]
    search_fields = [
        'student__first_name', 'student__last_name', 'student__roll_number',
        'fee_category__name', 'receipt_number'
    ]
    readonly_fields = ['remaining_amount', 'is_overdue']
    date_hierarchy = 'due_date'
    ordering = ['-due_date']


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ['title', 'priority', 'target_class', 'is_active', 'created_at']
    list_filter = ['priority', 'target_class', 'is_active', 'created_at']
    search_fields = ['title', 'content']
    ordering = ['-created_at']


@admin.register(StudentDocument)
class StudentDocumentAdmin(admin.ModelAdmin):
    list_display = ['student', 'document_type', 'title', 'uploaded_at']
    list_filter = ['document_type', 'uploaded_at', 'student__current_class']
    search_fields = [
        'student__first_name', 'student__last_name', 'student__roll_number',
        'title', 'description'
    ]
    ordering = ['-uploaded_at']


@admin.register(StudentPerformance)
class StudentPerformanceAdmin(admin.ModelAdmin):
    list_display = [
        'student', 'academic_year', 'semester', 'total_marks', 
        'obtained_marks', 'percentage', 'grade', 'rank'
    ]
    list_filter = [
        'academic_year', 'semester', 'grade', 'student__current_class'
    ]
    search_fields = [
        'student__first_name', 'student__last_name', 'student__roll_number'
    ]
    readonly_fields = ['percentage']
    ordering = ['-academic_year', '-semester', 'student']
