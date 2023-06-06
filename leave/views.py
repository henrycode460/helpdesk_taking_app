from django.shortcuts import render, redirect
from .forms import LeaveForm, EmployeeForm, DepartmentForm 
from django.contrib import messages
from datetime import datetime
from django.core.mail import EmailMessage

# Create your views here.


from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import DepartmentForm
from .models import Department, Leave
from django.conf import settings

def get_leave_url(request, leave):
    domain = request.get_host()
    accept_url = reverse('accept_leave', args=[leave.pk])  
    url = f"http://{domain}{accept_url}"
    
    return url



def create_leave(request):
    if request.method == 'POST':
        form = LeaveForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.created_by = request.user
            leave.status = 'Pending'
            leave.save()
          
            # Send email to supervisor
            subject = 'New Leave Request'
            message = f"Employee: {leave.employee} has requested a leave: {leave.leave_type}\nDescription: {leave.description}"
            message += f"\n\nView the leave request here: {get_leave_url(request, leave)}"  
            from_email = settings.DEFAULT_FROM_EMAIL
         
            supervisor_email = leave.employee.department.supervisor_email
            cc_list = ['jefftryer@gmail.com'] 

            email = EmailMessage(subject, message, from_email, [supervisor_email], cc=cc_list)
            email.send()
            
            messages.success(request, "Leave Created Successfully!!")
            return redirect('home')
        else:
            messages.warning(request, "Something went wrong. Please check the form.")

    else:
        form = LeaveForm()
        context = {'form': form}

    return render(request, 'create_leave.html', context)

def create_department(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
          
           
            
            messages.success(request, "Department Created Successfully!!")
            return redirect('home')
        else:
            messages.warning(request, "Something went wrong. Please check the form.")

    else:
        form = DepartmentForm()
        context = {'form': form}

    return render(request, 'create_department.html', context)



def create_employee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            # ... handle successful form submission

    else:
        form = EmployeeForm()

    return render(request, 'create_employee.html', {'form': form})


# def accept_leave(request, pk):
#     if request.user.is_supervisor:  
#         leave = Leave.objects.get(pk=pk)
#         leave.approver = request.user
#         leave.status = "Approved"
#         leave.approved_date = datetime.now()
#         leave.save()
#         messages.success(request, "Leave has been approved successfully, hope to see you soon!!")
#         return redirect('home')
#     else:
#         # Store the ticket ID in a session or temporary storage
#         # request.session['pending_ticket_id'] = pk
#         return redirect('login_page')

def accept_leave(request, pk):
    if request.user.is_supervisor:  
        leave = Leave.objects.get(pk=pk)
        leave.approver = request.user
        leave.status = "Approved"
        leave.approved_date = datetime.now()
        leave.save()
        
        # Send email to employee
        subject = 'Leave Request Approved'
        message = f"Your leave request has been approved."
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [leave.employee.employee_email]
        cc_list = ['jefftryer@gmail.com']  
        
        email = EmailMessage(subject, message, from_email, recipient_list, cc=cc_list)
        email.send()
        
        messages.success(request, "Leave has been approved successfully. Hope to see you soon!")
        return redirect('home')
    else:
        return redirect('login_page')


def pending_leave(request):
    if request.user.is_authenticated and request.user.is_supervisor:
        supervisor_email = request.user.email
    leave = Leave.objects.filter(employee__department__supervisor_email=supervisor_email, status='Pending').order_by('-created_at')
    
    context = {'leave': leave}
    return render(request, 'pending_leave.html', context)


