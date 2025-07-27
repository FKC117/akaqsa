from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
import re
from .models import (
    Student, Attendance, ClassRoutine, Exam, Result, 
    FeeCategory, Fee, Notice, StudentDocument, StudentPerformance, Class
)



def validate_bangladesh_phone(value):
    """Validate Bangladesh phone number format"""
    # Remove spaces, dashes, and parentheses
    phone = re.sub(r'[\s\-\(\)]', '', str(value))
    
    # Bangladesh phone number patterns:
    # +880 1XXXXXXXXX (with country code)
    # 01XXXXXXXXX (without country code)
    # 1XXXXXXXXX (without leading 0)
    
    if phone.startswith('+880'):
        phone = phone[4:]  # Remove +880
    
    if phone.startswith('0'):
        phone = phone[1:]  # Remove leading 0
    
    # Check if it's a valid Bangladesh mobile number
    if not re.match(r'^1[3-9]\d{8}$', phone):
        raise ValidationError(
            'Please enter a valid Bangladesh phone number. '
            'Format: +880 1XXXXXXXXX or 01XXXXXXXXX'
        )
    
    return value


class UserRegistrationForm(UserCreationForm):
    """Form for user registration"""
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    phone = forms.CharField(
        max_length=15, 
        required=True,
        validators=[validate_bangladesh_phone],
        help_text='Enter Bangladesh phone number (e.g., +880 1XXXXXXXXX or 01XXXXXXXXX)',
        widget=forms.TextInput(attrs={'placeholder': '+880 1XXXXXXXXX'})
    )
    address = forms.CharField(
        max_length=500,
        required=True,
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter your full address'})
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone', 'address', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('This email address is already in use.')
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        return validate_bangladesh_phone(phone)


class StudentRegistrationForm(forms.ModelForm):
    """Form for student registration"""
    class Meta:
        model = Student
        exclude = ['student_id', 'created_at', 'updated_at']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'admission_date': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
            'medical_conditions': forms.Textarea(attrs={'rows': 3}),
            'allergies': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_roll_number(self):
        roll_number = self.cleaned_data.get('roll_number')
        if Student.objects.filter(roll_number=roll_number).exists():
            raise ValidationError('This roll number is already taken.')
        return roll_number

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and Student.objects.filter(email=email).exists():
            raise ValidationError('This email address is already registered.')
        return email


class StudentUpdateForm(forms.ModelForm):
    """Form for updating student information"""
    class Meta:
        model = Student
        exclude = ['student_id', 'created_at', 'updated_at']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'admission_date': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
            'medical_conditions': forms.Textarea(attrs={'rows': 3}),
            'allergies': forms.Textarea(attrs={'rows': 3}),
        }


class AttendanceForm(forms.ModelForm):
    """Form for marking attendance"""
    class Meta:
        model = Attendance
        fields = ['student', 'date', 'is_present', 'reason']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'reason': forms.Textarea(attrs={'rows': 2}),
        }

    def clean(self):
        cleaned_data = super().clean()
        student = cleaned_data.get('student')
        date = cleaned_data.get('date')
        
        if student and date:
            # Check if attendance already exists for this student on this date
            existing_attendance = Attendance.objects.filter(
                student=student, date=date
            ).exclude(pk=self.instance.pk if self.instance.pk else None)
            
            if existing_attendance.exists():
                raise ValidationError(
                    f'Attendance for {student.full_name} on {date} already exists.'
                )
        
        return cleaned_data


class BulkAttendanceForm(forms.Form):
    """Form for bulk attendance marking"""
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    class_name = forms.ModelChoiceField(
        queryset=Class.objects.all(),
        empty_label="Select Class"
    )


class ClassRoutineForm(forms.ModelForm):
    """Form for class routine"""
    class Meta:
        model = ClassRoutine
        fields = ['class_name', 'subject', 'day', 'start_time', 'end_time', 'room_number', 'teacher_name']
        widgets = {
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        class_name = cleaned_data.get('class_name')
        day = cleaned_data.get('day')
        
        if start_time and end_time and start_time >= end_time:
            raise ValidationError('End time must be after start time.')
        
        if class_name and day and start_time:
            # Check for time conflicts
            conflicting_routines = ClassRoutine.objects.filter(
                class_name=class_name,
                day=day,
                start_time__lt=end_time,
                end_time__gt=start_time
            ).exclude(pk=self.instance.pk if self.instance.pk else None)
            
            if conflicting_routines.exists():
                raise ValidationError('This time slot conflicts with an existing routine.')
        
        return cleaned_data


class ExamForm(forms.ModelForm):
    """Form for exam creation"""
    class Meta:
        model = Exam
        fields = ['name', 'exam_type', 'subject', 'class_name', 'exam_date', 'total_marks', 'pass_marks', 'description']
        widgets = {
            'exam_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        total_marks = cleaned_data.get('total_marks')
        pass_marks = cleaned_data.get('pass_marks')
        
        if total_marks and pass_marks and pass_marks > total_marks:
            raise ValidationError('Pass marks cannot be greater than total marks.')
        
        return cleaned_data


class ResultForm(forms.ModelForm):
    """Form for entering exam results"""
    class Meta:
        model = Result
        fields = ['student', 'exam', 'marks_obtained', 'remarks']
        widgets = {
            'remarks': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_marks_obtained(self):
        marks_obtained = self.cleaned_data.get('marks_obtained')
        exam = self.cleaned_data.get('exam')
        
        if exam and marks_obtained and marks_obtained > exam.total_marks:
            raise ValidationError(f'Marks obtained cannot exceed total marks ({exam.total_marks}).')
        
        return marks_obtained


class FeeCategoryForm(forms.ModelForm):
    """Form for fee category"""
    class Meta:
        model = FeeCategory
        fields = ['name', 'amount', 'description', 'is_monthly']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class FeeForm(forms.ModelForm):
    """Form for fee management"""
    class Meta:
        model = Fee
        fields = [
            'student', 'fee_category', 'amount', 'due_date', 'paid_amount',
            'payment_date', 'payment_status', 'payment_method', 'receipt_number', 'remarks'
        ]
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'payment_date': forms.DateInput(attrs={'type': 'date'}),
            'remarks': forms.Textarea(attrs={'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        amount = cleaned_data.get('amount')
        paid_amount = cleaned_data.get('paid_amount')
        
        if amount and paid_amount and paid_amount > amount:
            raise ValidationError('Paid amount cannot exceed the total amount.')
        
        return cleaned_data


class NoticeForm(forms.ModelForm):
    """Form for school notices"""
    class Meta:
        model = Notice
        fields = ['title', 'content', 'priority', 'target_class', 'is_active']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5}),
        }


class StudentDocumentForm(forms.ModelForm):
    """Form for student documents"""
    class Meta:
        model = StudentDocument
        fields = ['student', 'document_type', 'title', 'file', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class StudentPerformanceForm(forms.ModelForm):
    """Form for student performance tracking"""
    class Meta:
        model = StudentPerformance
        fields = [
            'student', 'academic_year', 'semester', 'total_marks',
            'obtained_marks', 'grade', 'rank', 'remarks'
        ]
        widgets = {
            'remarks': forms.Textarea(attrs={'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        total_marks = cleaned_data.get('total_marks')
        obtained_marks = cleaned_data.get('obtained_marks')
        
        if total_marks and obtained_marks and obtained_marks > total_marks:
            raise ValidationError('Obtained marks cannot exceed total marks.')
        
        return cleaned_data


class StudentSearchForm(forms.Form):
    """Form for searching students"""
    search = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Search by name, ID, or roll number'})
    )
    class_name = forms.ModelChoiceField(
        queryset=Class.objects.all(),
        required=False,
        empty_label="All Classes"
    )
    gender = forms.ChoiceField(
        choices=[('', 'All')] + Student.GENDER_CHOICES,
        required=False
    )
    is_active = forms.ChoiceField(
        choices=[('', 'All'), ('True', 'Active'), ('False', 'Inactive')],
        required=False
    )


class AttendanceReportForm(forms.Form):
    """Form for generating attendance reports"""
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    class_name = forms.ModelChoiceField(
        queryset=Class.objects.all(),
        required=False,
        empty_label="All Classes"
    )
    student = forms.ModelChoiceField(
        queryset=Student.objects.all(),
        required=False,
        empty_label="All Students"
    )

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if start_date and end_date and start_date > end_date:
            raise ValidationError('Start date cannot be after end date.')
        
        return cleaned_data


class ResultReportForm(forms.Form):
    """Form for generating result reports"""
    exam = forms.ModelChoiceField(queryset=Exam.objects.all())
    class_name = forms.ModelChoiceField(
        queryset=Class.objects.all(),
        required=False,
        empty_label="All Classes"
    )
    min_percentage = forms.DecimalField(
        max_digits=5, decimal_places=2,
        required=False,
        min_value=0,
        max_value=100,
        widget=forms.NumberInput(attrs={'placeholder': 'Minimum percentage'})
    )
    max_percentage = forms.DecimalField(
        max_digits=5, decimal_places=2,
        required=False,
        min_value=0,
        max_value=100,
        widget=forms.NumberInput(attrs={'placeholder': 'Maximum percentage'})
    )


class FeeReportForm(forms.Form):
    """Form for generating fee reports"""
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    payment_status = forms.ChoiceField(
        choices=[('', 'All')] + Fee.PAYMENT_STATUS_CHOICES,
        required=False
    )
    fee_category = forms.ModelChoiceField(
        queryset=FeeCategory.objects.all(),
        required=False,
        empty_label="All Categories"
    )
    class_name = forms.ModelChoiceField(
        queryset=Class.objects.all(),
        required=False,
        empty_label="All Classes"
    ) 