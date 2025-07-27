// Main JavaScript for Al Aqsa School Management System

$(document).ready(function() {
    
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        $('.alert').fadeOut('slow');
    }, 5000);

    // Form validation enhancement
    $('form').on('submit', function() {
        var $form = $(this);
        var $submitBtn = $form.find('button[type="submit"]');
        
        // Disable submit button to prevent double submission
        $submitBtn.prop('disabled', true);
        $submitBtn.html('<span class="spinner-border spinner-border-sm me-2"></span>Processing...');
        
        // Re-enable after 3 seconds (in case of error)
        setTimeout(function() {
            $submitBtn.prop('disabled', false);
            $submitBtn.html($submitBtn.data('original-text') || 'Submit');
        }, 3000);
    });

    // Store original button text
    $('button[type="submit"]').each(function() {
        $(this).data('original-text', $(this).html());
    });

    // AJAX for getting students by class
    $('#id_class_name').on('change', function() {
        var classId = $(this).val();
        if (classId) {
            $.ajax({
                url: '/api/students-by-class/',
                data: {
                    'class_id': classId
                },
                success: function(data) {
                    var $studentSelect = $('#id_student');
                    $studentSelect.empty();
                    $studentSelect.append('<option value="">---------</option>');
                    
                    $.each(data.students, function(index, student) {
                        $studentSelect.append(
                            $('<option></option>').val(student.id).text(student.name + ' (' + student.roll_number + ')')
                        );
                    });
                }
            });
        }
    });

    // AJAX for getting subjects by class
    $('#id_class_name').on('change', function() {
        var classId = $(this).val();
        if (classId) {
            $.ajax({
                url: '/api/subjects-by-class/',
                data: {
                    'class_id': classId
                },
                success: function(data) {
                    var $subjectSelect = $('#id_subject');
                    $subjectSelect.empty();
                    $subjectSelect.append('<option value="">---------</option>');
                    
                    $.each(data.subjects, function(index, subject) {
                        $subjectSelect.append(
                            $('<option></option>').val(subject.id).text(subject.name + ' (' + subject.code + ')')
                        );
                    });
                }
            });
        }
    });

    // Bulk attendance functionality
    $('.attendance-checkbox').on('change', function() {
        var studentId = $(this).data('student-id');
        var isPresent = $(this).is(':checked');
        var reasonField = $('#reason_' + studentId);
        
        if (!isPresent) {
            reasonField.prop('required', true);
            reasonField.closest('.form-group').show();
        } else {
            reasonField.prop('required', false);
            reasonField.closest('.form-group').hide();
        }
    });

    // Search functionality
    $('#searchInput').on('keyup', function() {
        var value = $(this).val().toLowerCase();
        $('.searchable-row').filter(function() {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1);
        });
    });

    // Date picker enhancement
    $('input[type="date"]').each(function() {
        if (!$(this).val()) {
            $(this).val(new Date().toISOString().split('T')[0]);
        }
    });

    // Fee calculation
    $('#id_amount, #id_paid_amount').on('input', function() {
        var amount = parseFloat($('#id_amount').val()) || 0;
        var paidAmount = parseFloat($('#id_paid_amount').val()) || 0;
        var remainingAmount = amount - paidAmount;
        
        $('#remaining_amount').text('$' + remainingAmount.toFixed(2));
        
        // Update payment status
        var $statusSelect = $('#id_payment_status');
        if (paidAmount >= amount) {
            $statusSelect.val('Paid');
        } else if (paidAmount > 0) {
            $statusSelect.val('Partial');
        } else {
            $statusSelect.val('Pending');
        }
    });

    // Result calculation
    $('#id_marks_obtained, #id_exam').on('input change', function() {
        var marksObtained = parseFloat($('#id_marks_obtained').val()) || 0;
        var examId = $('#id_exam').val();
        
        if (examId) {
            // Get exam details via AJAX
            $.ajax({
                url: '/api/exam-details/',
                data: {
                    'exam_id': examId
                },
                success: function(data) {
                    var totalMarks = data.total_marks;
                    var percentage = (marksObtained / totalMarks) * 100;
                    var grade = calculateGrade(percentage);
                    
                    $('#percentage').text(percentage.toFixed(2) + '%');
                    $('#grade').text(grade);
                }
            });
        }
    });

    // Grade calculation function
    function calculateGrade(percentage) {
        if (percentage >= 90) return 'A+';
        else if (percentage >= 80) return 'A';
        else if (percentage >= 70) return 'B';
        else if (percentage >= 60) return 'C';
        else if (percentage >= 50) return 'D';
        else return 'F';
    }

    // Print functionality
    $('.print-btn').on('click', function() {
        window.print();
    });

    // Export to Excel functionality
    $('.export-excel').on('click', function() {
        var tableId = $(this).data('table');
        var table = document.getElementById(tableId);
        var html = table.outerHTML;
        var url = 'data:application/vnd.ms-excel,' + encodeURIComponent(html);
        var downloadLink = document.createElement("a");
        document.body.appendChild(downloadLink);
        downloadLink.href = url;
        downloadLink.download = tableId + '.xls';
        downloadLink.click();
        document.body.removeChild(downloadLink);
    });

    // Confirmation dialogs
    $('.delete-btn').on('click', function(e) {
        if (!confirm('Are you sure you want to delete this item?')) {
            e.preventDefault();
        }
    });

    // Auto-save form data
    $('form').on('input', function() {
        var formData = $(this).serialize();
        localStorage.setItem('form_autosave_' + this.id, formData);
    });

    // Restore form data on page load
    $('form').each(function() {
        var savedData = localStorage.getItem('form_autosave_' + this.id);
        if (savedData) {
            var form = this;
            var params = new URLSearchParams(savedData);
            params.forEach(function(value, key) {
                var field = form.querySelector('[name="' + key + '"]');
                if (field) {
                    field.value = value;
                }
            });
        }
    });

    // Clear saved form data on successful submission
    $('form').on('submit', function() {
        localStorage.removeItem('form_autosave_' + this.id);
    });

    // Real-time search with debouncing
    var searchTimeout;
    $('.live-search').on('input', function() {
        clearTimeout(searchTimeout);
        var $this = $(this);
        var searchTerm = $this.val();
        var searchUrl = $this.data('search-url');
        
        searchTimeout = setTimeout(function() {
            if (searchTerm.length >= 2) {
                $.ajax({
                    url: searchUrl,
                    data: {
                        'q': searchTerm
                    },
                    success: function(data) {
                        $this.siblings('.search-results').html(data);
                    }
                });
            } else {
                $this.siblings('.search-results').empty();
            }
        }, 300);
    });

    // Chart.js integration (if needed)
    if (typeof Chart !== 'undefined') {
        // Sample chart configuration
        var ctx = document.getElementById('attendanceChart');
        if (ctx) {
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                    datasets: [{
                        label: 'Attendance Rate',
                        data: [95, 92, 88, 94, 91, 89],
                        borderColor: 'rgb(75, 192, 192)',
                        tension: 0.1
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: {
                            beginAtZero: true,
                            max: 100
                        }
                    }
                }
            });
        }
    }

    // Notification system
    function showNotification(message, type = 'info') {
        var alertClass = 'alert-' + type;
        var alertHtml = `
            <div class="alert ${alertClass} alert-dismissible fade show" role="alert">
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `;
        
        $('.notifications-container').append(alertHtml);
        
        // Auto-remove after 5 seconds
        setTimeout(function() {
            $('.notifications-container .alert').last().fadeOut();
        }, 5000);
    }

    // Global notification function
    window.showNotification = showNotification;

    // Keyboard shortcuts
    $(document).on('keydown', function(e) {
        // Ctrl/Cmd + N for new student
        if ((e.ctrlKey || e.metaKey) && e.key === 'n') {
            e.preventDefault();
            window.location.href = '/student/create/';
        }
        
        // Ctrl/Cmd + S for save (if in a form)
        if ((e.ctrlKey || e.metaKey) && e.key === 's') {
            e.preventDefault();
            $('form:focus').submit();
        }
        
        // Escape to close modals
        if (e.key === 'Escape') {
            $('.modal').modal('hide');
        }
    });

    // Responsive table wrapper
    $('.table-responsive').each(function() {
        var $table = $(this).find('table');
        var $wrapper = $('<div class="table-wrapper"></div>');
        $table.wrap($wrapper);
    });

    // Loading states
    $('.btn-loading').on('click', function() {
        var $btn = $(this);
        var originalText = $btn.text();
        
        $btn.prop('disabled', true);
        $btn.html('<span class="spinner-border spinner-border-sm me-2"></span>Loading...');
        
        // Re-enable after 5 seconds
        setTimeout(function() {
            $btn.prop('disabled', false);
            $btn.text(originalText);
        }, 5000);
    });

    // Initialize any additional plugins or custom functionality
    initializeCustomFeatures();
});

// Custom features initialization
function initializeCustomFeatures() {
    // Add any additional initialization code here
    
    // Example: Initialize custom date picker
    if ($.fn.datepicker) {
        $('.datepicker').datepicker({
            format: 'yyyy-mm-dd',
            autoclose: true,
            todayHighlight: true
        });
    }
    
    // Example: Initialize select2 for better dropdowns
    if ($.fn.select2) {
        $('.select2').select2({
            theme: 'bootstrap-5'
        });
    }
}

// Utility functions
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

function formatDate(date) {
    return new Intl.DateTimeFormat('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    }).format(new Date(date));
}

function validateEmail(email) {
    var re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

function validatePhone(phone) {
    var re = /^[\+]?[1-9][\d]{0,15}$/;
    return re.test(phone.replace(/[\s\-\(\)]/g, ''));
} 