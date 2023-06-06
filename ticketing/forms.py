from django import forms
from .models import Ticket
# from django_select2 import forms as s2forms
from user.models import User
from django.utils import timezone




class NewTicketForm(forms.ModelForm):
      def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['assignee'].queryset = self.get_assignee_queryset()

      def get_assignee_queryset(self):
        # Filter technicians who don't have tickets with status 'Pending' or 'In_Progress'
          technicians = User.objects.filter(is_technician=True).exclude(ticket__status__in=['Pending', 'In_Progress']).distinct()

        # Filter technicians who are currently logged in
          # logged_in_technicians = technicians.filter(is_logged_in=True)

          # return logged_in_technicians
          return technicians
      
      class Meta:
        model = Ticket
        fields = ['customer', 'title', 'description', 'assignee']
        
        
class UpdateTicketForm(forms.ModelForm):
                                       
    class Meta:
        model = Ticket
        fields = ['customer', 'title', 'description', 'assignee']



class TechnicianFeedbackForm(forms.ModelForm):
    
    class Meta:
        model = Ticket
        fields = ['technician_remark', 'attachments']
        