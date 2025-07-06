from django.db import models
from django.utils import timezone
from django.conf import settings
from cloudinary_storage.storage import MediaCloudinaryStorage

cloudinary_storage_instance = MediaCloudinaryStorage()

EVENT_TYPES = (
    ('trip', 'Academic Trip'),
    ('game', 'Game Night'),
    ('workshop', 'Workshop'),
    ('conference', 'Conference'),
    ('other', 'Other'),
)

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    type = models.CharField(max_length=20, choices=EVENT_TYPES)
    location = models.CharField(max_length=200, blank=True, null=True)
    banner = models.ImageField(storage=cloudinary_storage_instance,upload_to='event_banners/', blank=True, null=True)
    registration_required = models.BooleanField(default=False)
    payment_required = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def is_upcoming(self):
        return self.date >= timezone.now()

    def __str__(self):
        return self.title
    
class EventBooking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    payment_status = models.CharField(max_length=20, choices=(
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('declined', 'Declined'),
    ), default='pending')
    transaction_code = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.event} ({self.payment_status})"
