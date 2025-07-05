from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Event, EventBooking
from accounts.models import PaymentSettings
from django.utils import timezone

@login_required
def event_booking_view(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    user = request.user

    bookings = EventBooking.objects.filter(user=user, event=event).order_by('-submitted_at')
    payment_settings = PaymentSettings.objects.first()

    if request.method == 'POST':
        amount = request.POST.get('amount')
        transaction_code = request.POST.get('transaction_code')

        if amount and transaction_code:
            if not EventBooking.objects.filter(transaction_code=transaction_code).exists():
                EventBooking.objects.create(
                    user=user,
                    event=event,
                    amount=amount,
                    transaction_code=transaction_code,
                    payment_status='pending',
                )
                messages.success(request, "✅ Payment submitted successfully. Awaiting approval.")
                return redirect('event_booking', event_id=event.id)
            else:
                messages.error(request, "⚠️ A payment with this transaction code already exists.")
        else:
            messages.warning(request, "⚠️ Please fill all payment fields.")

    approved_booking = bookings.filter(payment_status='approved').first()
    latest_booking = bookings.first()  # latest booking or None

    context = {
        'event': event,
        'bookings': bookings,
        'approved_booking': approved_booking,
        'latest_booking': latest_booking,
        'payment_settings': payment_settings,
    }
    return render(request, 'events/booking.html', context)


@login_required
def past_events_view(request):
    past_events = Event.objects.filter(date__lt=timezone.now()).order_by('-date')
    return render(request, 'events/past_events.html', {'past_events': past_events})
