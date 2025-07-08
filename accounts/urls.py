from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .forms import  MyPasswordResetForm

urlpatterns = [
    path('', views.home_view, name='home'),
    path('read-more/', views.read_more, name='read_more'),
    path('contact_us/',views.contact_view, name='contact_us'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('dash/',views.dashboard_view, name='dashboard'),
    path('register-member/', views.register_member_view, name='register_member'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html',form_class= MyPasswordResetForm, email_template_name='accounts/password_reset_email.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),
]
