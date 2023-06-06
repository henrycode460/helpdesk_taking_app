from django.contrib import admin

# Register your models here.



# # Register your models here.

from .models import Leave, Employee, Department

admin.site.register(Leave)
admin.site.register(Employee)
admin.site.register(Department)
