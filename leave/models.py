
from django.db import models
from user.models import User

# Create your models here.


#department
class Department(models.Model):
    
     DeptList = ( 
        
        ('Finance', 'Finance'),
        ('Operation', 'Operation'),
        ('Technical', 'Technical'),
        ('Customer Service', 'Customer Service'),
        ('Sales & Marketing', 'Sales & Marketing'),
	    ('NOC', 'NOC'),	
	    ('Procurement', 'Procurement'),
	    ('Enterprise_Solution', 'Enterprise Solution'),
     
         )
     
     name = models.CharField(max_length=50, choices=DeptList, default='Technical')
     supervisor_email = models.EmailField(null=True, blank=True)
   
     def __str__(self):
        return self.name
    

#  # Employee classs
    
class Employee(models.Model):
        
        full_name = models.CharField( max_length=55)
        employee_email = models.EmailField(null=True, blank=True)
        department = models.ForeignKey(Department, on_delete=models.CASCADE)
        address = models.CharField( max_length=100)
        date_hire = models.DateField(auto_now=False, auto_now_add=False)
        phone_number = models.CharField(max_length=50)
        position = models.CharField( max_length=100)
  
        def __str__(self):
         return self.full_name



class Leave(models.Model):
    LeaveType = ( 
        ('Privilege/Annual Leave', 'Privilege/Annual Leave'),
        ('Medical Leave', 'Medical Leave'),
      
       
     )
    
    LeaveStatus = ( 
        ('PENDING', 'Pending'),           
        ('APPROVED', 'Approved'),
        ('DENINED', 'Denined'),
      
       
     )
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    leave_type = models.CharField(max_length=50, choices=LeaveType, default='Privilege/Annanual Leave')
    status = models.CharField(max_length=50, choices=LeaveStatus, default='Privilege/Annanual Leave' )
    description = models.TextField(max_length=300, null=True, blank=True)
    approver = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField('created at', auto_now_add=True)
    approved_date = models.DateTimeField(null=True, blank=True)
    denied_date = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField('updated at', auto_now=True)
    
    def __str__(self):
      return self.employee.__str__() 
  
  
  

