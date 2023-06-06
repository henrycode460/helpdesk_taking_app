from django.contrib.auth.decorators import login_required
from ticketing.models import Ticket




@login_required
def get_pending_tickets_count(request):
    count = Ticket.objects.filter(assignee=request.user, status='Pending').count()
    return {'pending_tickets_count': count} if count > 0 else {}

@login_required
def get_unassigned_tickets_count(request):
    count = Ticket.objects.filter( status='Pending').count()
    return {'unassigned_tickets_count': count} if count > 0 else {}

