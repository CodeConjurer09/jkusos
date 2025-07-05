from django.urls import path
from . import views

urlpatterns = [
    path('booking/<int:event_id>/', views.event_booking_view, name='event_booking'),   
    path('events/past/', views.past_events_view, name='past_events'),
]
