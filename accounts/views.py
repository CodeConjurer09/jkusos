from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import CustomRegisterForm, CustomLoginForm, MembershipPaymentForm, MyPasswordResetForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import MembershipPayment, PaymentSettings, UserQuestion, ContactSettings, ContactMessage
from events.models import Event
from django.utils import timezone
from django.db.models import Sum
from django.contrib.sites.shortcuts import get_current_site


def home_view(request):
    return render(request, 'homepage.html')
def read_more(request):
    return render(request, 'about_detail.html')

def register_view(request):
    if request.method == 'POST':
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully. You can now login.')
            return redirect('login')
        else:
            messages.error(request, 'Registration failed. Please check your creditions and try again.')
    else:
        form = CustomRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful, Redirecting you to the dashboard.')
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid email or password')
    else:
        form = CustomLoginForm()
    return render(request, 'accounts/login.html', {'form': form})
    
@login_required
def register_member_view(request):
    if request.method == 'POST':
        form = MembershipPaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.user = request.user
            payment.save()
            messages.success(request, "Payment submitted. Awaiting approval.")
            return redirect('dashboard')
    else:
        form = MembershipPaymentForm()
    return render(request, 'accounts/register_member.html', {'form': form})

@login_required
def dashboard_view(request):
    user = request.user
    upcoming_events = Event.objects.filter(date__gte=timezone.now()).order_by('date')
    latest_payment = MembershipPayment.objects.filter(user=user).order_by('-submitted_at').first()
    payment_settings = PaymentSettings.objects.last()

    # Sum of approved payments
    total_approved_amount = MembershipPayment.objects.filter(
        user=user, status=MembershipPayment.STATUS_APPROVED
    ).aggregate(total=Sum('amount'))['total'] or 0

    # Questions asked by user
    user_questions = UserQuestion.objects.filter(user=user).order_by('-submitted_at')

    # Allowed event types for booking
    allowed_booking_types = ['trip', 'workshop', 'conference']

    if request.method == 'POST':
        if 'question' in request.POST:
            question_text = request.POST.get('question')
            if question_text:
                UserQuestion.objects.create(user=user, question=question_text)
                messages.success(request, "✅ Your question has been submitted.", extra_tags='question')
            else:
                messages.error(request, "⚠️ Please enter a question.", extra_tags='question')

        elif 'transaction_code' in request.POST:
            amount = request.POST.get('amount')
            transaction_code = request.POST.get('transaction_code')
            if amount and transaction_code:
                if not MembershipPayment.objects.filter(transaction_code=transaction_code).exists():
                    MembershipPayment.objects.create(
                        user=user,
                        amount=amount,
                        transaction_code=transaction_code,
                        status=MembershipPayment.STATUS_PENDING,
                    )
                    messages.success(request, "✅ Payment submitted successfully. Awaiting approval.", extra_tags='payment')
                else:
                    messages.error(request, "⚠️ A payment with this transaction code already exists.", extra_tags='payment')
            else:
                messages.warning(request, "⚠️ Fill in all payment fields.", extra_tags='payment')

            return redirect('dashboard')

    context = {
        'user': user,
        'upcoming_events': upcoming_events,
        'latest_payment': latest_payment,
        'payment_settings': payment_settings,
        'total_approved_amount': total_approved_amount,
        'user_questions': user_questions,
        'allowed_booking_types': allowed_booking_types,  # added for template use
    }
    return render(request, 'accounts/dashboard.html', context)

def contact_view(request):
    contact_info = ContactSettings.objects.last()  # get latest contact details

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        if name and email and message:
            ContactMessage.objects.create(name=name, email=email, message=message)
            messages.success(request, "✅ Your message has been sent successfully.")
        else:
            messages.error(request, "⚠️ Please fill all fields.")

    return render(request, 'contact.html', {
        'contact_info': contact_info
    })

def custom_password_reset_view(request):
    if request.method == 'POST':
        form = MyPasswordResetForm(request.POST)
        if form.is_valid():
            domain = get_current_site(request).domain
            form.save(domain=domain, protocol='https')  # You can pass your custom email template too
            messages.success(request, "A reset link has been sent to your email.")
            return redirect('password_reset')
    else:
        form = MyPasswordResetForm()
    return render(request, 'accounts/password_reset.html', {'form': form})


