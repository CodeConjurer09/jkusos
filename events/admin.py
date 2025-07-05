from django.contrib import admin
from .models import Event, EventBooking

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'date', 'registration_required', 'payment_required')
    list_filter = ('type', 'registration_required', 'payment_required')
    search_fields = ('title', 'description', 'location')



@admin.register(EventBooking)
class EventBookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'payment_status', 'amount', 'transaction_code', 'submitted_at')
    list_filter = ('payment_status', 'event')
    search_fields = ('user__username', 'transaction_code', 'event__title')
    readonly_fields = ('submitted_at',)

    actions = ['approve_bookings', 'decline_bookings']

    def approve_bookings(self, request, queryset):
        updated = queryset.update(payment_status='approved')
        self.message_user(request, f"{updated} booking(s) marked as approved.")
    approve_bookings.short_description = "Mark selected bookings as Approved"

    def decline_bookings(self, request, queryset):
        updated = queryset.update(payment_status='declined')
        self.message_user(request, f"{updated} booking(s) marked as declined.")
    decline_bookings.short_description = "Mark selected bookings as Declined"