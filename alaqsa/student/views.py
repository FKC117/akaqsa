from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.db.models import Q, Count, Sum, Avg
from django.http import HttpResponse, JsonResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils import timezone
from django.core.paginator import Paginator
from datetime import datetime, timedelta
import json

from .models import (
    Student, Attendance, ClassRoutine, Exam, Result, 
    FeeCategory, Fee, Notice, StudentDocument, StudentPerformance, Subject, Class
)
from .forms import (
    UserRegistrationForm, StudentRegistrationForm, StudentUpdateForm,
    AttendanceForm, BulkAttendanceForm, ClassRoutineForm, ExamForm,
    ResultForm, FeeCategoryForm, FeeForm, NoticeForm, StudentDocumentForm,
    StudentPerformanceForm, StudentSearchForm, AttendanceReportForm,
    ResultReportForm, FeeReportForm
)


def register(request):
    """User registration view"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'student/register.html', {'form': form})


@login_required
def dashboard(request):
    """Main dashboard view"""
    # Get current date
    today = timezone.now().date()
    
    # Dashboard statistics
    total_students = Student.objects.filter(is_active=True).count()
    total_classes = Student.objects.values('current_class').distinct().count()
    today_attendance = Attendance.objects.filter(date=today, is_present=True).count()
    pending_fees = Fee.objects.filter(payment_status='Pending').count()
    
    # Recent activities
    recent_students = Student.objects.filter(is_active=True).order_by('-created_at')[:5]
    recent_notices = Notice.objects.filter(is_active=True).order_by('-created_at')[:5]
    upcoming_exams = Exam.objects.filter(exam_date__gte=today).order_by('exam_date')[:5]
    
    # Fee statistics
    total_fees_due = Fee.objects.filter(payment_status='Pending').aggregate(
        total=Sum('amount')
    )['total'] or 0
    total_fees_collected = Fee.objects.filter(payment_status='Paid').aggregate(
        total=Sum('paid_amount')
    )['total'] or 0
    
    context = {
        'total_students': total_students,
        'total_classes': total_classes,
        'today_attendance': today_attendance,
        'pending_fees': pending_fees,
        'recent_students': recent_students,
        'recent_notices': recent_notices,
        'upcoming_exams': upcoming_exams,
        'total_fees_due': total_fees_due,
        'total_fees_collected': total_fees_collected,
    }
    
    return render(request, 'student/dashboard.html', context)


# Student Views
class StudentListView(LoginRequiredMixin, ListView):
    """List view for students with search and filtering"""
    model = Student
    template_name = 'student/student_list.html'
    context_object_name = 'students'
    paginate_by = 20

    def get_queryset(self):
        queryset = Student.objects.filter(is_active=True)
        
        # Search functionality
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(student_id__icontains=search) |
                Q(roll_number__icontains=search)
            )
        
        # Filter by class
        class_name = self.request.GET.get('class_name')
        if class_name:
            queryset = queryset.filter(current_class=class_name)
        
        # Filter by gender
        gender = self.request.GET.get('gender')
        if gender:
            queryset = queryset.filter(gender=gender)
        
        # Filter by status
        is_active = self.request.GET.get('is_active')
        if is_active:
            queryset = queryset.filter(is_active=is_active == 'True')
        
        return queryset.order_by('current_class', 'roll_number')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = StudentSearchForm(self.request.GET)
        context['classes'] = Student.objects.values_list('current_class', flat=True).distinct()
        return context


class StudentDetailView(LoginRequiredMixin, DetailView):
    """Detail view for student"""
    model = Student
    template_name = 'student/student_detail.html'
    context_object_name = 'student'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = self.get_object()
        
        # Get student's attendance
        context['attendance_count'] = Attendance.objects.filter(
            student=student, is_present=True
        ).count()
        
        # Get student's results
        context['results'] = Result.objects.filter(student=student).order_by('-created_at')[:10]
        
        # Get student's fees
        context['fees'] = Fee.objects.filter(student=student).order_by('-due_date')[:10]
        
        # Get student's documents
        context['documents'] = StudentDocument.objects.filter(student=student).order_by('-uploaded_at')
        
        return context


class StudentCreateView(LoginRequiredMixin, CreateView):
    """Create view for student"""
    model = Student
    form_class = StudentRegistrationForm
    template_name = 'student/student_form.html'
    success_url = reverse_lazy('student:student_list')

    def form_valid(self, form):
        messages.success(self.request, 'Student registered successfully!')
        return super().form_valid(form)


class StudentUpdateView(LoginRequiredMixin, UpdateView):
    """Update view for student"""
    model = Student
    form_class = StudentUpdateForm
    template_name = 'student/student_form.html'
    success_url = reverse_lazy('student:student_list')

    def form_valid(self, form):
        messages.success(self.request, 'Student information updated successfully!')
        return super().form_valid(form)


class StudentDeleteView(LoginRequiredMixin, DeleteView):
    """Delete view for student"""
    model = Student
    template_name = 'student/student_confirm_delete.html'
    success_url = reverse_lazy('student:student_list')

    def delete(self, request, *args, **kwargs):
        student = self.get_object()
        student.is_active = False
        student.save()
        messages.success(request, 'Student deactivated successfully!')
        return redirect(self.success_url)


# Attendance Views
@login_required
def attendance_list(request):
    """List view for attendance"""
    attendances = Attendance.objects.all().order_by('-date')
    
    # Filter by date range
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    if start_date:
        attendances = attendances.filter(date__gte=start_date)
    if end_date:
        attendances = attendances.filter(date__lte=end_date)
    
    # Filter by class (id)
    class_id = request.GET.get('class_name')
    if class_id:
        attendances = attendances.filter(student__current_class__id=class_id)

    paginator = Paginator(attendances, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'classes': Class.objects.all(),
    }
    
    return render(request, 'student/attendance_list.html', context)


@login_required
def attendance_create(request):
    """Create attendance record"""
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Attendance recorded successfully!')
            return redirect('student:attendance_list')
    else:
        form = AttendanceForm()
    
    context = {
        'form': form,
        'classes': Class.objects.all(),
        'today': timezone.now().date(),
    }
    
    return render(request, 'student/attendance_form.html', context)


@login_required
def attendance_update(request, pk):
    """Update attendance record"""
    attendance = get_object_or_404(Attendance, pk=pk)
    
    if request.method == 'POST':
        # Handle form submission
        date = request.POST.get('date')
        is_present = request.POST.get('is_present') == 'True'
        reason = request.POST.get('reason', '')
        
        attendance.date = date
        attendance.is_present = is_present
        attendance.reason = reason
        attendance.save()
        
        messages.success(request, 'Attendance updated successfully!')
        return redirect('student:attendance_list')
    
    return redirect('student:attendance_list')


@login_required
def attendance_delete(request, pk):
    """Delete attendance record"""
    attendance = get_object_or_404(Attendance, pk=pk)
    
    if request.method == 'POST':
        attendance.delete()
        messages.success(request, 'Attendance record deleted successfully!')
        return redirect('student:attendance_list')
    
    return redirect('student:attendance_list')


@login_required
def bulk_attendance(request):
    """Bulk attendance marking"""
    if request.method == 'POST':
        form = BulkAttendanceForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            class_obj = form.cleaned_data['class_name']
            
            students = Student.objects.filter(current_class=class_obj, is_active=True)
            
            # Handle attendance submission
            if 'submit_attendance' in request.POST:
                for student in students:
                    student_id = f"student_{student.id}"
                    is_present = request.POST.get(student_id) == 'present'
                    reason = request.POST.get(f"reason_{student.id}", '')
                    
                    # Create or update attendance
                    attendance, created = Attendance.objects.get_or_create(
                        student=student,
                        date=date,
                        defaults={'is_present': is_present, 'reason': reason}
                    )
                    
                    if not created:
                        attendance.is_present = is_present
                        attendance.reason = reason
                        attendance.save()
                
                messages.success(request, 'Bulk attendance recorded successfully!')
                return redirect('student:attendance_list')
            
            context = {
                'students': students,
                'date': date,
                'class_name': class_obj,
            }
            return render(request, 'student/bulk_attendance.html', context)
    else:
        form = BulkAttendanceForm()
    
    return render(request, 'student/bulk_attendance_form.html', {'form': form})


# Class Routine Views
class ClassRoutineListView(LoginRequiredMixin, ListView):
    """List view for class routines"""
    model = ClassRoutine
    template_name = 'student/class_routine_list.html'
    context_object_name = 'routines'

    def get_queryset(self):
        queryset = ClassRoutine.objects.all()
        
        # Filter by class
        class_name = self.request.GET.get('class_name')
        if class_name:
            queryset = queryset.filter(class_name=class_name)
        
        return queryset.order_by('class_name', 'day', 'start_time')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['classes'] = Student.objects.values_list('current_class', flat=True).distinct()
        return context


class ClassRoutineCreateView(LoginRequiredMixin, CreateView):
    """Create view for class routine"""
    model = ClassRoutine
    form_class = ClassRoutineForm
    template_name = 'student/class_routine_form.html'
    success_url = reverse_lazy('student:class_routine_list')

    def form_valid(self, form):
        messages.success(self.request, 'Class routine created successfully!')
        return super().form_valid(form)


# Exam and Result Views
class ExamListView(LoginRequiredMixin, ListView):
    """List view for exams"""
    model = Exam
    template_name = 'student/exam_list.html'
    context_object_name = 'exams'

    def get_queryset(self):
        queryset = Exam.objects.all()
        
        # Filter by exam type
        exam_type = self.request.GET.get('exam_type')
        if exam_type:
            queryset = queryset.filter(exam_type=exam_type)
        
        # Filter by class
        class_name = self.request.GET.get('class_name')
        if class_name:
            queryset = queryset.filter(class_name=class_name)
        
        return queryset.order_by('-exam_date')


class ExamCreateView(LoginRequiredMixin, CreateView):
    """Create view for exam"""
    model = Exam
    form_class = ExamForm
    template_name = 'student/exam_form.html'
    success_url = reverse_lazy('student:exam_list')

    def form_valid(self, form):
        messages.success(self.request, 'Exam created successfully!')
        return super().form_valid(form)


@login_required
def result_list(request):
    """List view for results"""
    results = Result.objects.all().order_by('-created_at')
    
    # Filter by exam
    exam_id = request.GET.get('exam')
    if exam_id:
        results = results.filter(exam_id=exam_id)
    
    # Filter by class
    class_name = request.GET.get('class_name')
    if class_name:
        results = results.filter(student__current_class=class_name)
    
    paginator = Paginator(results, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'exams': Exam.objects.all(),
        'classes': Student.objects.values_list('current_class', flat=True).distinct(),
    }
    
    return render(request, 'student/result_list.html', context)


@login_required
def result_create(request):
    """Create result record"""
    if request.method == 'POST':
        form = ResultForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Result recorded successfully!')
            return redirect('student:result_list')
    else:
        form = ResultForm()
    
    return render(request, 'student/result_form.html', {'form': form})


# Fee Views
class FeeCategoryListView(LoginRequiredMixin, ListView):
    """List view for fee categories"""
    model = FeeCategory
    template_name = 'student/fee_category_list.html'
    context_object_name = 'categories'


class FeeCategoryCreateView(LoginRequiredMixin, CreateView):
    """Create view for fee category"""
    model = FeeCategory
    form_class = FeeCategoryForm
    template_name = 'student/fee_category_form.html'
    success_url = reverse_lazy('student:fee_category_list')

    def form_valid(self, form):
        messages.success(self.request, 'Fee category created successfully!')
        return super().form_valid(form)


@login_required
def fee_list(request):
    """List view for fees"""
    fees = Fee.objects.all().order_by('-due_date')
    
    # Filter by payment status
    status = request.GET.get('status')
    if status:
        fees = fees.filter(payment_status=status)
    
    # Filter by class
    class_name = request.GET.get('class_name')
    if class_name:
        fees = fees.filter(student__current_class=class_name)
    
    paginator = Paginator(fees, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'classes': Student.objects.values_list('current_class', flat=True).distinct(),
    }
    
    return render(request, 'student/fee_list.html', context)


@login_required
def fee_create(request):
    """Create fee record"""
    if request.method == 'POST':
        form = FeeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fee record created successfully!')
            return redirect('student:fee_list')
    else:
        form = FeeForm()
    
    return render(request, 'student/fee_form.html', {'form': form})


# Notice Views
class NoticeListView(LoginRequiredMixin, ListView):
    """List view for notices"""
    model = Notice
    template_name = 'student/notice_list.html'
    context_object_name = 'notices'

    def get_queryset(self):
        return Notice.objects.filter(is_active=True).order_by('-created_at')


class NoticeCreateView(LoginRequiredMixin, CreateView):
    """Create view for notice"""
    model = Notice
    form_class = NoticeForm
    template_name = 'student/notice_form.html'
    success_url = reverse_lazy('student:notice_list')

    def form_valid(self, form):
        messages.success(self.request, 'Notice created successfully!')
        return super().form_valid(form)


# Report Views
@login_required
def attendance_report(request):
    """Generate attendance report"""
    if request.method == 'POST':
        form = AttendanceReportForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            class_name = form.cleaned_data['class_name']
            student = form.cleaned_data['student']
            
            # Build query
            attendances = Attendance.objects.filter(date__range=[start_date, end_date])
            
            if class_name:
                attendances = attendances.filter(student__current_class=class_name)
            
            if student:
                attendances = attendances.filter(student=student)
            
            # Calculate statistics
            total_days = (end_date - start_date).days + 1
            total_attendance = attendances.filter(is_present=True).count()
            total_absent = attendances.filter(is_present=False).count()
            
            context = {
                'form': form,
                'attendances': attendances,
                'start_date': start_date,
                'end_date': end_date,
                'total_days': total_days,
                'total_attendance': total_attendance,
                'total_absent': total_absent,
                'attendance_percentage': (total_attendance / (total_attendance + total_absent)) * 100 if (total_attendance + total_absent) > 0 else 0,
            }
            
            return render(request, 'student/attendance_report.html', context)
    else:
        form = AttendanceReportForm()
    
    return render(request, 'student/attendance_report_form.html', {'form': form})


@login_required
def result_report(request):
    """Generate result report"""
    if request.method == 'POST':
        form = ResultReportForm(request.POST)
        if form.is_valid():
            exam = form.cleaned_data['exam']
            class_name = form.cleaned_data['class_name']
            min_percentage = form.cleaned_data['min_percentage']
            max_percentage = form.cleaned_data['max_percentage']
            
            # Build query
            results = Result.objects.filter(exam=exam)
            
            if class_name:
                results = results.filter(student__current_class=class_name)
            
            if min_percentage:
                results = results.filter(marks_obtained__gte=(exam.total_marks * min_percentage / 100))
            
            if max_percentage:
                results = results.filter(marks_obtained__lte=(exam.total_marks * max_percentage / 100))
            
            # Calculate statistics
            total_students = results.count()
            passed_students = results.filter(marks_obtained__gte=exam.pass_marks).count()
            average_marks = results.aggregate(avg=Avg('marks_obtained'))['avg'] or 0
            
            context = {
                'form': form,
                'results': results,
                'exam': exam,
                'total_students': total_students,
                'passed_students': passed_students,
                'failed_students': total_students - passed_students,
                'pass_percentage': (passed_students / total_students) * 100 if total_students > 0 else 0,
                'average_marks': average_marks,
            }
            
            return render(request, 'student/result_report.html', context)
    else:
        form = ResultReportForm()
    
    return render(request, 'student/result_report_form.html', {'form': form})


@login_required
def fee_report(request):
    """Generate fee report"""
    if request.method == 'POST':
        form = FeeReportForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            payment_status = form.cleaned_data['payment_status']
            fee_category = form.cleaned_data['fee_category']
            class_name = form.cleaned_data['class_name']
            
            # Build query
            fees = Fee.objects.filter(due_date__range=[start_date, end_date])
            
            if payment_status:
                fees = fees.filter(payment_status=payment_status)
            
            if fee_category:
                fees = fees.filter(fee_category=fee_category)
            
            if class_name:
                fees = fees.filter(student__current_class=class_name)
            
            # Calculate statistics
            total_amount = fees.aggregate(total=Sum('amount'))['total'] or 0
            total_paid = fees.aggregate(total=Sum('paid_amount'))['total'] or 0
            total_pending = total_amount - total_paid
            
            context = {
                'form': form,
                'fees': fees,
                'start_date': start_date,
                'end_date': end_date,
                'total_amount': total_amount,
                'total_paid': total_paid,
                'total_pending': total_pending,
                'collection_percentage': (total_paid / total_amount) * 100 if total_amount > 0 else 0,
            }
            
            return render(request, 'student/fee_report.html', context)
    else:
        form = FeeReportForm()
    
    return render(request, 'student/fee_report_form.html', {'form': form})


# API Views for AJAX
@login_required
def get_students_by_class(request):
    """Get students by class for AJAX requests"""
    class_id = request.GET.get('class_id')
    if class_id:
        students = Student.objects.filter(current_class_id=class_id, is_active=True)
        data = [{'id': student.id, 'name': student.full_name, 'roll_number': student.roll_number} for student in students]
        return JsonResponse({'students': data})
    return JsonResponse({'students': []})


@login_required
def get_subjects_by_class(request):
    """Get subjects by class for AJAX requests"""
    class_id = request.GET.get('class_id')
    if class_id:
        subjects = Subject.objects.filter(classroutine__class_name_id=class_id).distinct()
        data = [{'id': subject.id, 'name': subject.name, 'code': subject.code} for subject in subjects]
        return JsonResponse({'subjects': data})
    return JsonResponse({'subjects': []})
