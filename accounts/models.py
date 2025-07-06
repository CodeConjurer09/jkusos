from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings

class UserManager(BaseUserManager):
    def create_user(self, email, reg_number, first_name, last_name, password=None):
        if not email:
            raise ValueError("Users must have an email address.")
        user = self.model(
            email=self.normalize_email(email),
            reg_number=reg_number,
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, reg_number, first_name, last_name, password=None):
        user = self.create_user(email, reg_number, first_name, last_name, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
    
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    reg_number = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_member = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['reg_number', 'first_name', 'last_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

class MembershipPayment(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_APPROVED = 'approved'
    STATUS_DECLINED = 'declined'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_APPROVED, 'Approved'),
        (STATUS_DECLINED, 'Declined'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_code = models.CharField(max_length=20, unique=True)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
    )
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.transaction_code} - {self.get_status_display()}"

class PaymentSettings(models.Model):
    paybill_number = models.CharField(max_length=20)
    account_name = models.CharField(max_length=50)
    account_number = models.CharField(max_length=20)


    def __str__(self):
        return f"Paybill: {self.paybill_number} | Account: {self.account_name} | Account_name {self.account_number}"

    class Meta:
        verbose_name = "Payment Setting"
        verbose_name_plural = "Payment Settings"

class UserQuestion(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    question = models.TextField()
    reply = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    answered = models.BooleanField(default=False)

    def __str__(self):
        return f"Question from {self.user.email} - {self.submitted_at.strftime('%Y-%m-%d %H:%M')}"


class ContactSettings(models.Model):
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    website = models.URLField(null=True, blank=True)
    instagram = models.URLField(null=True, blank=True)
    whatsapp_group = models.URLField(null=True, blank=True)

    def __str__(self):
        return "JKUSOS Contact Settings"

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.email}) - {self.submitted_at:%Y-%m-%d}"