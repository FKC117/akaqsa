# Al Aqsa School Management System

A comprehensive Django-based school management system designed to handle student information, attendance, results, fees, and more.

## Features

### 🎓 Student Management
- **Student Registration**: Complete student profile creation with personal, academic, and contact information
- **Student Search & Filter**: Advanced search functionality with multiple filter options
- **Student Profiles**: Detailed student information with photo upload
- **Document Management**: Upload and manage student documents
- **Student Performance Tracking**: Monitor academic progress over time

### 📊 Attendance Management
- **Daily Attendance**: Mark individual student attendance
- **Bulk Attendance**: Mark attendance for entire classes at once
- **Attendance Reports**: Generate detailed attendance reports with statistics
- **Absence Tracking**: Record reasons for absences

### 📚 Academic Management
- **Class Management**: Create and manage school classes
- **Subject Management**: Organize subjects with codes and descriptions
- **Class Routines**: Create and manage class schedules
- **Exam Management**: Schedule and manage exams
- **Result Management**: Record and track student results
- **Grade Calculation**: Automatic grade calculation based on marks

### 💰 Fee Management
- **Fee Categories**: Create different fee categories (tuition, transport, etc.)
- **Fee Records**: Track individual student fee payments
- **Payment Status**: Monitor payment status (Paid, Pending, Partial, Overdue)
- **Fee Reports**: Generate comprehensive fee collection reports
- **Receipt Generation**: Generate payment receipts

### 📢 Communication
- **Notice Board**: Post and manage school notices
- **Priority Notices**: Categorize notices by priority level
- **Targeted Notices**: Send notices to specific classes

### 📈 Reporting & Analytics
- **Dashboard**: Comprehensive overview with key statistics
- **Attendance Reports**: Detailed attendance analysis
- **Result Reports**: Academic performance analysis
- **Fee Reports**: Financial collection reports
- **Export Functionality**: Export data to Excel format
- **Print Support**: Print-friendly reports

### 🔐 Security & Authentication
- **User Registration**: Secure user account creation
- **Login/Logout**: Django's built-in authentication system
- **Password Validation**: Strong password requirements
- **Session Management**: Secure session handling

## Technology Stack

- **Backend**: Django 5.2.4
- **Database**: MySQL
- **Frontend**: Bootstrap 5, jQuery
- **Icons**: Font Awesome 6
- **Forms**: Django Crispy Forms
- **File Handling**: Pillow (for images)
- **Reports**: ReportLab (PDF), OpenPyXL (Excel)

## Installation & Setup

### Prerequisites
- Python 3.8+
- MySQL Server
- pip (Python package manager)

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd alaqsa-school-system
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Database Setup
1. Create a MySQL database:
```sql
CREATE DATABASE alaqsa CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

2. Update database settings in `alaqsa/alaqsa/settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'alaqsa',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### Step 5: Run Migrations
```bash
cd alaqsa
python manage.py makemigrations
python manage.py migrate
```

### Step 6: Create Superuser
```bash
python manage.py createsuperuser
```

### Step 7: Collect Static Files
```bash
python manage.py collectstatic
```

### Step 8: Run the Development Server
```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## Initial Setup

### 1. Create Classes
- Go to Admin Panel → Classes
- Add school classes (e.g., Class 1-A, Class 2-B, etc.)

### 2. Create Subjects
- Go to Admin Panel → Subjects
- Add subjects with codes (e.g., Mathematics - MATH001)

### 3. Create Fee Categories
- Go to Admin Panel → Fee Categories
- Add fee categories (e.g., Monthly Tuition, Transport Fee)

### 4. Add Students
- Use the web interface to add students
- Or use the Admin Panel for bulk operations

## Usage Guide

### For Administrators

#### Dashboard
- View key statistics and recent activities
- Quick access to common functions
- Monitor fee collection and attendance

#### Student Management
1. **Add Student**: Fill in all required information
2. **Search Students**: Use the search bar or filters
3. **Edit Student**: Update student information
4. **View Details**: See complete student profile

#### Attendance Management
1. **Mark Attendance**: Use bulk attendance for efficiency
2. **View Reports**: Generate attendance reports
3. **Track Absences**: Record absence reasons

#### Fee Management
1. **Create Fee Records**: Assign fees to students
2. **Record Payments**: Update payment status
3. **Generate Reports**: Monitor collection

### For Teachers

#### Class Routine
- View class schedules
- Manage subject timings

#### Results Management
- Enter exam results
- Calculate grades automatically
- Generate result reports

## File Structure

```
alaqsa/
├── alaqsa/                 # Main project directory
│   ├── alaqsa/            # Project settings
│   │   ├── settings.py    # Django settings
│   │   ├── urls.py        # Main URL configuration
│   │   └── ...
│   ├── student/           # Student app
│   │   ├── models.py      # Database models
│   │   ├── views.py       # View functions
│   │   ├── forms.py       # Form definitions
│   │   ├── admin.py       # Admin interface
│   │   └── urls.py        # App URL patterns
│   ├── templates/         # HTML templates
│   │   ├── base.html      # Base template
│   │   └── student/       # Student templates
│   ├── static/            # Static files
│   │   ├── css/           # Stylesheets
│   │   ├── js/            # JavaScript files
│   │   └── images/        # Images
│   └── manage.py          # Django management script
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Database Models

### Core Models
- **Student**: Complete student information
- **Class**: School classes and sections
- **Subject**: Academic subjects
- **Attendance**: Daily attendance records
- **ClassRoutine**: Class schedules
- **Exam**: Exam definitions
- **Result**: Student exam results
- **FeeCategory**: Fee types
- **Fee**: Individual fee records
- **Notice**: School notices
- **StudentDocument**: Student documents
- **StudentPerformance**: Academic performance tracking

## API Endpoints

### AJAX Endpoints
- `/api/students-by-class/`: Get students by class
- `/api/subjects-by-class/`: Get subjects by class

### Report Endpoints
- `/report/attendance/`: Attendance reports
- `/report/result/`: Result reports
- `/report/fee/`: Fee reports

## Customization

### Adding New Features
1. Create new models in `student/models.py`
2. Add corresponding views in `student/views.py`
3. Create forms in `student/forms.py`
4. Add URL patterns in `student/urls.py`
5. Create templates in `templates/student/`

### Styling
- Modify `static/css/style.css` for custom styles
- Update Bootstrap classes in templates
- Add custom JavaScript in `static/js/main.js`

## Security Considerations

- All forms include CSRF protection
- User authentication required for all views
- File upload validation
- SQL injection protection through Django ORM
- XSS protection through template escaping

## Deployment

### Production Settings
1. Set `DEBUG = False` in settings
2. Configure production database
3. Set up static file serving
4. Configure email settings
5. Set up HTTPS

### Environment Variables
```bash
export SECRET_KEY='your-secret-key'
export DATABASE_URL='mysql://user:pass@host:port/db'
export DEBUG='False'
```

## Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Check MySQL service is running
   - Verify database credentials
   - Ensure database exists

2. **Static Files Not Loading**
   - Run `python manage.py collectstatic`
   - Check static file settings

3. **Migration Errors**
   - Delete migration files and recreate
   - Check model field changes

4. **Import Errors**
   - Ensure virtual environment is activated
   - Check all dependencies are installed

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation

## Future Enhancements

- [ ] Parent/Guardian portal
- [ ] Student portal
- [ ] SMS/Email notifications
- [ ] Mobile app
- [ ] Advanced analytics
- [ ] Multi-language support
- [ ] Online payment integration
- [ ] Library management
- [ ] Transport management
- [ ] Staff management

---

**Al Aqsa School Management System** - Empowering education through technology. 