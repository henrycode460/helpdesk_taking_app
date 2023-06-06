from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
# from user.models import User
from .models import Ticket
from datetime import datetime
# from django.db.models import Q
from django.contrib.auth.decorators import login_required
from user.models import User
# Create your views here.
from .forms import NewTicketForm, UpdateTicketForm, TechnicianFeedbackForm
# from .filters import TicketFilter
# import csv
# from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.core.paginator import Paginator



from django.core.mail import send_mail
from django.conf import settings
# from django.contrib.sites.shortcuts import get_current_site
from twilio.rest import Client
from django.urls import reverse
from .filters import TicketFilter, TicketFilterCustomer


def get_ticket_url(request, ticket):
    domain = request.get_host()
    accept_url = reverse('accept_ticket', args=[ticket.pk])  
    url = f"http://{domain}{accept_url}"
    
    return url

from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import redirect, render
from django.contrib import messages

def add_ticket(request):
    if request.method == 'POST':
        form = NewTicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.created_by = request.user
            ticket.status = 'Pending'
            form.save()

            # Send email to technician
            subject = 'New Ticket Assignment'
            message = f'A new ticket has been assigned to you. Ticket Name: {ticket.title}\nDescription: {ticket.description}\nCustomerName: {ticket.customer}'
            message += f'\n\nView the ticket here: {get_ticket_url(request, ticket)}'  # the ticket URL
            from_email = settings.DEFAULT_FROM_EMAIL

            if ticket.assignee and ticket.assignee.email:
                technician_email = ticket.assignee.email
                send_mail(subject, message, from_email, [technician_email])

                # Send WhatsApp message to technician
                # technician = ticket.assignee
                # if technician:
                #     phone_number = '+233269124517'
                #     whatsapp_message = f"You have been assigned a new ticket.\nTicket Name: {ticket.title}\nDescription: {ticket.description}\nAccept the ticket: {request.build_absolute_uri(reverse('accept_ticket', args=[ticket.pk]))}"
                #     send_whatsapp_message(phone_number, whatsapp_message)

                # If WhatsApp message couldn't be sent, fallback to email
                # if not send_whatsapp_message:
                #     send_mail(subject, message, from_email, [technician_email])

                messages.success(request, "Ticket created successfully. A technician will be assigned soon!")
                return redirect('home')
            else:
                messages.warning(request, "Ticket created successfully. No technician assigned.")
                return redirect('home')
        else:
            messages.warning(request, "Something went wrong. Please check the form.")
    else:
        form = NewTicketForm()

    context = {'form': form}
    return render(request, 'add_ticket.html', context)

def update_ticket(request, pk):
    ticket = Ticket.objects.get(pk=pk)
    
    if not ticket.is_resolve:
        if request.method == 'POST':
          form = UpdateTicketForm(request.POST, instance=ticket)
          if form.is_valid():
            form.save()
            messages.success(request, "Ticket Successfully updated!!")
            return redirect('home')
          else:
            messages.warning(request, "Something went wrong check the output")
        else:
           form = UpdateTicketForm(instance=ticket)
         
           context = {'form': form}
    
           return render(request, 'update_ticket.html', context)

    else:
     messages.warning("You can't Update this ticket")
     return redirect('home')



def all_ticket_created(request):
    user = request.user
    ticket = Ticket.objects.filter(created_by=user)
    myfilter = TicketFilterCustomer(request.GET, queryset=ticket, request=request)

    #pargination
    p = Paginator(myfilter.qs, 8) 
    page = request.GET.get('page')
    tickets_parginating = p.get_page(page)
    nums = 'a' * tickets_parginating.paginator.num_pages
    context = { 'ticket': ticket, 'myfilter' : myfilter, 'tickets_parginating': tickets_parginating, 'nums': nums}
   
    return render(request, 'all_ticket_created.html', context)


# def send_whatsapp_message(message, phone_number):
#     account_sid = 'AC7b4a7847406e0dfbd448cfe6792a3681'
#     auth_token = '7e4832d9cde4f2cc1f769b027797f30b'
#     client = Client(account_sid, auth_token)

#     message = client.messages.create(
#         from_='whatsapp:+14155238886',
#          body=message,
#         to= phone_number
        
#     )

#     return message.sid

def accept_ticket(request, pk):
    if request.user.is_technician:
        ticket = Ticket.objects.get(pk=pk)
        ticket.assignee = request.user
        ticket.status = "In_Progress"
        ticket.accepted_date = datetime.now()
        ticket.save()

        # Send email to customer care
        customer_care_email = ticket.created_by.email
        subject_care = 'Ticket Accepted'
        technician_name = request.user.get_username()
        message_care = f'The ticket "{ticket.title}" has been accepted by {technician_name}.'
        send_mail(subject_care, message_care, settings.DEFAULT_FROM_EMAIL, [customer_care_email])

        # Send email to customer
        customer_email = ticket.customer.email
        subject_customer = f'Update on Ticket: {ticket.customer.name}'
        message_customer = f'Hello {ticket.customer.name},\n\n'
        message_customer += f'Your issue with Ticket Number {ticket.ticket_number} is currently being attended to by our Technical Support Team. We will get back to you shortly. \n\n'
        message_customer += 'Thanks for your patience.\n\n'
        message_customer += 'Best Regards,\n'
        message_customer += 'Telecel Customer Support.'
        send_mail(subject_customer, message_customer, settings.DEFAULT_FROM_EMAIL, [customer_email])

        messages.success(request, "Ticket has been accepted successfully, kindly resolve as soon as possible!!")
        return redirect('ticket_in_progress')
    else:
        # Store the ticket ID in a session or temporary storage
        # request.session['pending_ticket_id'] = pk
        return redirect('ticket_queue')


def ticket_to_claim_cs(request):
    user = request.user
    ticket = Ticket.objects.filter(assignee__isnull=True, created_by=user).order_by('-date_created')
    
    context = {'ticket': ticket}
    return render(request, 'ticket_to_claim_cs.html', context)

def ticket_intergration_cs(request):
    user = request.user
    ticket = Ticket.objects.filter(status="Pending", created_by=user)
    ticketunassigned = Ticket.objects.filter(assignee__isnull=True, created_by=user)
    
    
    # chart------------------------------------------
    
    ticker_created_no = Ticket.objects.filter(status="Pending", created_by=user).count()
    ticker_created_no = int(ticker_created_no)
    
    ticket_unassigned_no = Ticket.objects.filter(assignee__isnull=True, created_by=user).count()
    ticket_unassigned_no = int( ticket_unassigned_no)
    

    
    status_list = ['Ticket Created', 'Unassigned Ticket']
    status_number = [ticker_created_no, ticket_unassigned_no]
    
    #chart end--------------------------------------------------------
    
    
    context = {'ticket': ticket, 'ticketunassigned': ticketunassigned,'ticker_created_no': ticker_created_no, 'ticket_unassigned_no': ticket_unassigned_no, 'status_list': status_list, 'status_number': status_number}
    
    return render(request, 'ticket_intergration_cs.html', context)


def ticket_queue(request):
    ticket = Ticket.objects.filter(assignee=request.user,status='Pending').order_by('-date_created')
    
    context = {'ticket': ticket}
    return render(request, 'ticket_queue.html', context)


def technicain_feedback (request, pk):
    ticket = Ticket.objects.get(pk=pk)
    
    if not ticket.is_resolve :
        if request.method == 'POST':
          form = TechnicianFeedbackForm(request.POST, instance=ticket)
          if form.is_valid():
            form.save()
            messages.success(request, "Feedback added successfully!!")
            return redirect('technicain_feedback', ticket.pk)
          else:
            messages.warning(request, "Something went wrong check the output")
        else:
           form = TechnicianFeedbackForm(instance=ticket)
         
           context = {'form': form , 'ticket' : ticket}
    
           return render(request, 'technicain_feedback.html', context)

    else:
     messages.warning("your Feedback can't be added")
     return redirect('technicain_feedback')
 
def ticket_details(request, pk):
    tickets = Ticket.objects.get(pk=pk)
    
    context = {'ticket': tickets }
    return render(request, 'ticket_details.html', context)

def postpone_ticket(request, pk):
     ticket = Ticket.objects.get(pk=pk)
     ticket.status = "Postpone"
     ticket.postpone_date = datetime.now()
     ticket.save()
     messages.success(request, "You have Postpone this ticket successfully!!")
     return redirect('home')
 
def cancel_ticket(request, pk):
     ticket = Ticket.objects.get(pk=pk)
     ticket.status = "Cancel"
     ticket.cancel_date = datetime.now()
     ticket.save()
     
     messages.success(request, "You have cancel this ticket successfully!!")
     return redirect('home')
 
def close_ticket(request, pk):
     ticket = Ticket.objects.get(pk=pk)
     ticket.status = "Completed"
     ticket.is_resolve = True
     ticket.close_date = datetime.now()
     ticket.save()
     messages.success(request, "Ticket has been resolved, thanks for your support!!")
     return redirect('ticket_queue')

def ticket_in_progress(request):
    ticket = Ticket.objects.filter(assignee=request.user, is_resolve=False, status="In_Progress").order_by('-accepted_date')
    context = {'ticket': ticket }
    return render(request, 'ticket_in_progress.html', context)



def all_ticket_created_tech(request):
    user = request.user
    ticket = Ticket.objects.filter(assignee=user)
    myfilter = TicketFilter(request.GET, queryset=ticket, request=request)

    #pargination
    p = Paginator(myfilter.qs, 8) 
    page = request.GET.get('page')
    tickets_parginating = p.get_page(page)
    nums = 'a' * tickets_parginating.paginator.num_pages
    context = { 'ticket': ticket, 'myfilter' : myfilter, 'tickets_parginating': tickets_parginating, 'nums': nums}
   
    return render(request, 'all_ticket_created_tech.html', context)



def ticket_to_claim_tech(request):
    
    ticket = Ticket.objects.filter(assignee__isnull=True).order_by('-date_created')
    
    context = {'ticket': ticket}
    return render(request, 'ticket_to_claim_tech.html', context)
