from django.urls import path



from . import views
  
urlpatterns = [
path('add_ticket/', views.add_ticket, name='add_ticket'),
path('accept_ticket/<int:pk>/', views.accept_ticket, name='accept_ticket'),
path('all_ticket_created/', views.all_ticket_created, name='all_ticket_created'),
path('ticket_to_claim_cs/', views.ticket_to_claim_cs, name="ticket_to_claim_cs"),
path('ticket_intergration_cs/', views.ticket_intergration_cs, name="ticket_intergration_cs"),
path('ticket_queue/', views.ticket_queue, name="ticket_queue"),
path('update_ticket/<int:pk>', views.update_ticket, name="update_ticket"),
path('technicain_feedback/<int:pk>', views.technicain_feedback, name='technicain_feedback'),
path('ticket_details/<int:pk>', views.ticket_details, name="ticket_details"),
path('postpone_ticket/<int:pk>', views.postpone_ticket, name="postpone_ticket"),
path('cancel_ticket/<int:pk>/', views.cancel_ticket, name="cancel_ticket"),
path('close_ticket/<int:pk>', views.close_ticket, name="close_ticket"),
path('ticket_in_progress/', views.ticket_in_progress, name="ticket_in_progress"),
path('all_ticket_created_tech/', views.all_ticket_created_tech, name='all_ticket_created_tech'),
path('ticket_to_claim_tech/', views.ticket_to_claim_tech, name='ticket_to_claim_tech'),



  
     
     
 ]