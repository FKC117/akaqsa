
from django.urls import path
from . import views

app_name = 'student'

urlpatterns = [
    # Authentication
    path('register/', views.register, name='register'),
    
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Student URLs
    path('', views.StudentListView.as_view(), name='student_list'),
    path('student/<int:pk>/', views.StudentDetailView.as_view(), name='student_detail'),
    path('student/create/', views.StudentCreateView.as_view(), name='student_create'),
    path('student/<int:pk>/update/', views.StudentUpdateView.as_view(), name='student_update'),
    path('student/<int:pk>/delete/', views.StudentDeleteView.as_view(), name='student_delete'),
    
    # Attendance URLs
    path('attendance/', views.attendance_list, name='attendance_list'),
    path('attendance/create/', views.attendance_create, name='attendance_create'),
    path('attendance/<int:pk>/update/', views.attendance_update, name='attendance_update'),
    path('attendance/<int:pk>/delete/', views.attendance_delete, name='attendance_delete'),
    path('attendance/bulk/', views.bulk_attendance, name='bulk_attendance'),
    
    # Class Routine URLs
    path('routine/', views.ClassRoutineListView.as_view(), name='class_routine_list'),
    path('routine/create/', views.ClassRoutineCreateView.as_view(), name='class_routine_create'),
    
    # Exam URLs
    path('exam/', views.ExamListView.as_view(), name='exam_list'),
    path('exam/create/', views.ExamCreateView.as_view(), name='exam_create'),
    
    # Result URLs
    path('result/', views.result_list, name='result_list'),
    path('result/create/', views.result_create, name='result_create'),
    
    # Fee URLs
    path('fee-category/', views.FeeCategoryListView.as_view(), name='fee_category_list'),
    path('fee-category/create/', views.FeeCategoryCreateView.as_view(), name='fee_category_create'),
    path('fee/', views.fee_list, name='fee_list'),
    path('fee/create/', views.fee_create, name='fee_create'),
    
    # Notice URLs
    path('notice/', views.NoticeListView.as_view(), name='notice_list'),
    path('notice/create/', views.NoticeCreateView.as_view(), name='notice_create'),
    
    # Report URLs
    path('report/attendance/', views.attendance_report, name='attendance_report'),
    path('report/result/', views.result_report, name='result_report'),
    path('report/fee/', views.fee_report, name='fee_report'),
    
    # API URLs for AJAX
    path('api/students-by-class/', views.get_students_by_class, name='get_students_by_class'),
    path('api/subjects-by-class/', views.get_subjects_by_class, name='get_subjects_by_class'),
]