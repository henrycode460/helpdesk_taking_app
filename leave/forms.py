from django import forms
from .models import Department, Employee, Leave

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'supervisor_email']
        widgets = {
            'name': forms.Select(choices=Department.DeptList),
        }


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['full_name', 'employee_email', 'department', 'address', 'date_hire', 'phone_number', 'position']
        widgets = {
            'department': forms.Select(attrs={'class': 'form-control'}),
        }
        
        
class LeaveForm(forms.ModelForm):
    class Meta:
        model = Leave
        fields = ['employee', 'leave_type', 'description']
        widgets = {
            'leave_type': forms.Select(choices=Leave.LeaveType),
            'status': forms.Select(choices=Leave.LeaveStatus),
        }