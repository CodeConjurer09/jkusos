from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('read-more/', views.read_more, name='read_more'),
    path('contact_us/',views.contact_view, name='contact_us'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('dash/',views.dashboard_view, name='dashboard'),
    path('register-member/', views.register_member_view, name='register_member'),
]
