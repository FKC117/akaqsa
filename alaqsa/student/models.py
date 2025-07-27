from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
import uuid


class Class(models.Model):
    """Model for school classes"""
    name = models.CharField(max_length=50, unique=True)
    section = models.CharField(max_length=10)
    capacity = models.PositiveIntegerField(default=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Classes"
        unique_together = ['name', 'section']

    def __str__(self):
        return f"{self.name}-{self.section}"

    @property
    def total_students(self):
        return self.student_set.count()


class Subject(models.Model):
    """Model for school subjects"""
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.code})"


class Student(models.Model):
    """Model for student information"""
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]

    # Basic Information
    student_id = models.CharField(max_length=6, unique=True, blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES, blank=True)
    
    # Contact Information
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=10)
    
    # Academic Information
    current_class = models.ForeignKey(Class, on_delete=models.CASCADE)
    admission_date = models.DateField()
    roll_number = models.CharField(max_length=20, unique=True)
    
    # Parent/Guardian Information
    father_name = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100)
    parent_phone = models.CharField(max_length=15)
    parent_email = models.EmailField(blank=True)
    
    # Emergency Contact
    emergency_contact_name = models.CharField(max_length=100)
    emergency_contact_phone = models.CharField(max_length=15)
    emergency_contact_relation = models.CharField(max_length=50)
    
    # Medical Information
    medical_conditions = models.TextField(blank=True)
    allergies = models.TextField(blank=True)
    
    # Documents
    photo = models.ImageField(upload_to='student_photos/', blank=True)
    birth_certificate = models.FileField(upload_to='documents/', blank=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['current_class', 'roll_number']

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.student_id})"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def age(self):
        from datetime import date
        today = date.today()
        return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))

    def save(self, *args, **kwargs):
        if not self.student_id:
            # Generate a 6-digit student ID
            last_student = Student.objects.order_by('-student_id').first()
            if last_student and last_student.student_id.isdigit():
                last_id = int(last_student.student_id)
                new_id = str(last_id + 1).zfill(6)
            else:
                new_id = '000001'
            self.student_id = new_id
        super().save(*args, **kwargs)


class Attendance(models.Model):
    """Model for student attendance"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    is_present = models.BooleanField(default=True)
    reason = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['student', 'date']
        ordering = ['-date']

    def __str__(self):
        status = "Present" if self.is_present else "Absent"
        return f"{self.student.full_name} - {self.date} - {status}"


class ClassRoutine(models.Model):
    """Model for class routine/schedule"""
    DAY_CHOICES = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]

    class_name = models.ForeignKey(Class, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    day = models.CharField(max_length=10, choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    room_number = models.CharField(max_length=20, blank=True)
    teacher_name = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['class_name', 'day', 'start_time']

    def __str__(self):
        return f"{self.class_name} - {self.subject} - {self.day} ({self.start_time}-{self.end_time})"


class Exam(models.Model):
    """Model for exams"""
    EXAM_TYPE_CHOICES = [
        ('Midterm', 'Midterm'),
        ('Final', 'Final'),
        ('Quiz', 'Quiz'),
        ('Assignment', 'Assignment'),
        ('Project', 'Project'),
    ]

    name = models.CharField(max_length=100)
    exam_type = models.CharField(max_length=20, choices=EXAM_TYPE_CHOICES)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE)
    exam_date = models.DateField()
    total_marks = models.PositiveIntegerField()
    pass_marks = models.PositiveIntegerField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject} - {self.class_name}"


class Result(models.Model):
    """Model for student results"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2)
    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['student', 'exam']

    def __str__(self):
        return f"{self.student.full_name} - {self.exam.name} - {self.marks_obtained}"

    @property
    def percentage(self):
        return (self.marks_obtained / self.exam.total_marks) * 100

    @property
    def grade(self):
        percentage = self.percentage
        if percentage >= 90:
            return 'A+'
        elif percentage >= 80:
            return 'A'
        elif percentage >= 70:
            return 'B'
        elif percentage >= 60:
            return 'C'
        elif percentage >= 50:
            return 'D'
        else:
            return 'F'

    @property
    def is_pass(self):
        return self.marks_obtained >= self.exam.pass_marks


class FeeCategory(models.Model):
    """Model for fee categories"""
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    is_monthly = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - ${self.amount}"


class Fee(models.Model):
    """Model for student fees"""
    PAYMENT_STATUS_CHOICES = [
        ('Paid', 'Paid'),
        ('Pending', 'Pending'),
        ('Partial', 'Partial'),
        ('Overdue', 'Overdue'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('Cash', 'Cash'),
        ('Check', 'Check'),
        ('Bank Transfer', 'Bank Transfer'),
        ('Online', 'Online'),
        ('Card', 'Card'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    fee_category = models.ForeignKey(FeeCategory, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_date = models.DateField(null=True, blank=True)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='Pending')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, blank=True)
    receipt_number = models.CharField(max_length=50, blank=True)
    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-due_date']

    def __str__(self):
        return f"{self.student.full_name} - {self.fee_category.name} - {self.payment_status}"

    @property
    def remaining_amount(self):
        return self.amount - self.paid_amount

    @property
    def is_overdue(self):
        return self.due_date < timezone.now().date() and self.payment_status != 'Paid'


class Notice(models.Model):
    """Model for school notices"""
    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Urgent', 'Urgent'),
    ]

    title = models.CharField(max_length=200)
    content = models.TextField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='Medium')
    target_class = models.ForeignKey(Class, on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.priority}"


class StudentDocument(models.Model):
    """Model for student documents"""
    DOCUMENT_TYPE_CHOICES = [
        ('Birth Certificate', 'Birth Certificate'),
        ('Transfer Certificate', 'Transfer Certificate'),
        ('Character Certificate', 'Character Certificate'),
        ('Medical Certificate', 'Medical Certificate'),
        ('Other', 'Other'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    document_type = models.CharField(max_length=50, choices=DOCUMENT_TYPE_CHOICES)
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='student_documents/')
    description = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.full_name} - {self.document_type}"


class StudentPerformance(models.Model):
    """Model for tracking student performance over time"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    academic_year = models.CharField(max_length=9)  # e.g., "2023-2024"
    semester = models.CharField(max_length=20, blank=True)
    total_marks = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    obtained_marks = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    grade = models.CharField(max_length=2, blank=True)
    rank = models.PositiveIntegerField(null=True, blank=True)
    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['student', 'academic_year', 'semester']
        ordering = ['-academic_year', '-semester']

    def __str__(self):
        return f"{self.student.full_name} - {self.academic_year} - {self.percentage}%"

    def save(self, *args, **kwargs):
        if self.total_marks > 0:
            self.percentage = (self.obtained_marks / self.total_marks) * 100
        super().save(*args, **kwargs)
