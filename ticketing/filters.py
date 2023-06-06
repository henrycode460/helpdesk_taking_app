import django_filters
from . models import *



class TicketFilter(django_filters.FilterSet):
    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        if request:
            self.filters['assignee'].queryset = User.objects.filter(username=request.user.username)

    assignee = django_filters.ModelChoiceFilter(
        field_name='assignee',
        queryset=User.objects.none(),  # Placeholder queryset, updated dynamically in __init__
        label='Assignee'
    )

    class Meta:
        model = Ticket
        fields = ['customer', 'assignee', 'status', 'created_by', 'date_created']

import django_filters

class TicketFilterCustomer(django_filters.FilterSet):
    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        if request:
            self.filters['created_by'].queryset = User.objects.filter(username=request.user.username)

    created_by = django_filters.ModelChoiceFilter(
        field_name='created_by',
        queryset=User.objects.none(),  # Placeholder queryset, updated dynamically in __init__
        label='Created By'
    )

    class Meta:
        model = Ticket
        fields = ['customer', 'assignee', 'status', 'created_by', 'date_created']

