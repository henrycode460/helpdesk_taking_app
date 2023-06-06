from django.shortcuts import render, redirect
from ticketing.models import Ticket


from django.contrib import messages
from django.forms import inlineformset_factory
from django.contrib.auth.models import User, auth
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm


# Create your views here.

def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password1")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Set the is_logged_in attribute to True
            user.is_logged_in = True
            user.save()

            login(request, user)
            # Check if there is a pending ticket ID stored in the session
            if 'pending_ticket_id' in request.session:
                pending_ticket_id = request.session.pop('pending_ticket_id')
                return redirect('accept_ticket', pk=pending_ticket_id)
            else:
                return redirect("home")
        else:
            messages.info(request, 'Username or password is incorrect')

    
    return render(request, 'log_in.html', {})


def home( request):
    tickets = Ticket.objects.filter(assignee=request.user, status="Pending")
    ticketUnassigned = Ticket.objects.filter(status="Pending")
    
    context = {'tickets': tickets , 'ticketUnassigned': ticketUnassigned}
    return render(request, 'base.html', context)


# def base( request):
#     tickets = Ticket.objects.filter(assignee=request.user, status="Pending")
    
#     context = {'tickets': tickets}
#     return render(request, 'base.html', context)



def registration_page(request):
    form = CreateUserForm()
    
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.info(request, "Account was created for" + " " + user)
                return redirect('login_page')
      
    context = {'form' : form}
    
    return render(request, 'registration_page.html', context)

def logout_user(request):
    # Update the is_logged_in attribute to False for the logged-out user
     if request.user.is_authenticated:
        request.user.is_logged_in = False
        request.user.save()

    # Perform the logout operation
     logout(request)
  
    
     return redirect('login_page')
 
 




