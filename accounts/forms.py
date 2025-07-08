from django import forms
from .models import User
from .models import MembershipPayment
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives

class CustomRegisterForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'})
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm password'})
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'reg_number']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
            'reg_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Registration Number'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already in use.")
        return email

    def clean_password2(self):
        p1 = self.cleaned_data.get('password1')
        p2 = self.cleaned_data.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Passwords do not match.")
        return p2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('password1'))
        if commit:
            user.save()
        return user

class CustomLoginForm(forms.Form):
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        })
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password'
        })
    )

class MembershipPaymentForm(forms.ModelForm):
    class Meta:
        model = MembershipPayment
        fields = ['transaction_code' , 'amount']

User = get_user_model()

class MyPasswordResetForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        max_length=254,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email address'
        })
    )

    def clean_email(self):
        email = self.cleaned_data['email']
        self.user = User.objects.filter(email__iexact=email, is_active=True).first()
        if not self.user:
            raise forms.ValidationError(_("No account is associated with this email."))
        return email

    def save(self, domain_override=None,
             subject_template_name='accounts/password_reset_subject.txt',
             email_template_name='accounts/password_reset_email.html',
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None, html_email_template_name=None,
             extra_email_context=None, **kwargs):
        """
        Generates a one-use only link for resetting password and sends to the user.
        """
        user = self.user
        if not user:
            return

        if domain_override:
            domain = domain_override
        else:
            current_site = get_current_site(request)
            domain = current_site.domain

        protocol = 'https' if use_https else 'http'
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = token_generator.make_token(user)

        context = {
            'email': user.email,
            'domain': domain,
            'site_name': getattr(current_site, 'name', domain) if not domain_override else domain,
            'uid': uid,
            'user': user,
            'token': token,
            'protocol': protocol,
            'reset_url': f"{protocol}://{domain}/reset/{uid}/{token}/",
        }

        if extra_email_context:
            context.update(extra_email_context)

        subject = render_to_string(subject_template_name, context)
        subject = ''.join(subject.splitlines())

        text_content = f"""
Hi {user.first_name},

We received a request to reset your password.
Click the link below to reset it:
{context['reset_url']}

If you didn’t request this, ignore this email.

Thanks,
JKUSOS Team
"""

        html_content = render_to_string(html_email_template_name or email_template_name, context)

        msg = EmailMultiAlternatives(subject, text_content, from_email, [user.email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
