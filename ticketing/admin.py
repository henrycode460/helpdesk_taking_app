
from django.contrib import admin

# # Register your models here.

from .models import Customer, Ticket

admin.site.register(Customer)
# admin.site.register(Employee)
admin.site.register(Ticket)


