from django.db import models
import uuid



# # Create your models here.

from django.db import models
# from django.contrib.auth.models import User
from user.models import User

# # Create your models here.

 

# #customer
class Customer(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    contact = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    services = models.CharField(max_length=100)
    payment_type = models.CharField(max_length=50)
    created_at = models.DateTimeField('created at', auto_now_add=True )
    updated_at = models.DateTimeField('updated at', auto_now=True )
    
    def __str__(self):
        return self.name
    
 

# # Ticket class

class Ticket(models.Model):
    
    
    TicketStatus = (
        ('Pending', 'Pending'),
        ('In_Progress', 'In Progress'),
	    ('Completed', 'Completed'),
	    ('Cancel', 'Cancel'),
        ('Postpone', 'Postpone'),	
	)
    
    Title= ( 
        ('New Installation', 'New Installation'),
        ('Support', 'Support'),
	    ('Re-Connection', 'Re-Connection'),
	    	
	)
    
    
    ticket_number = models.UUIDField(default= uuid.uuid4)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, choices=Title, default='Support')
    description = models.TextField()
    assignee = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_by')
    status = models.CharField(max_length=50, choices=TicketStatus, default='Pending')
    date_created = models.DateTimeField( auto_now_add=True)
    updated_at = models.DateTimeField( auto_now=True )
    is_resolve = models.BooleanField(default=False)
    accepted_date = models.DateTimeField(null=True, blank=True)
    accepted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='accepted_tickets')
    close_date = models.DateTimeField(null=True, blank=True)
    cancel_date = models.DateTimeField(null=True, blank=True)
    postpone_date = models.DateTimeField(null=True, blank=True)
    technician_remark = models.TextField(max_length=300, null=True, blank=True)
    attachments = models.FileField(null=True, blank=True)
    
    
    def __str__(self):
        return self.title
    

    
    
    



