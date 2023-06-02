from django.urls import path
from django.contrib.auth import views as auth_views
# from user.forms import EmailValidationOnForgotPassword


from . import views
  
urlpatterns = [
    path('', views.login_page, name="login_page"),
    path('registration_page/', views.registration_page, name='registration_page'),
    path('home/', views.home, name='home'),
    path('logout_view/', views.logout_user, name="logout_user"),
    # path('technician_page/', views.technician_page, name="technician_page"),
    # path('reset_password/', auth_views.PasswordResetView.as_view(template_name='password-reset.html'), name="reset_password" ),
    # path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name="password_reset_done"),
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name="password_reset_confirm" ),
    # path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name="password_reset_complete"),
    # path('user/password_reset/', auth_views.PasswordResetView.as_view(form_class=EmailValidationOnForgotPassword), name='password_reset'),
    
 ]