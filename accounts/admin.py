from django.contrib import admin
import openpyxl
from io import BytesIO
from django.http import HttpResponse
from django.db import models
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, MembershipPayment, PaymentSettings, UserQuestion, ContactSettings, ContactMessage, ClubOfficial


class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'reg_number', 'is_member', 'is_staff', 'is_active')
    list_filter = ('is_member', 'is_staff', 'is_superuser')
    search_fields = ('email', 'reg_number', 'first_name', 'last_name')
    ordering = ('email',)
    actions = ['export_to_excel']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'reg_number')}),
        ('Membership', {'fields': ('is_member',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important Dates', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'reg_number', 'first_name', 'last_name', 'password1', 'password2')}
        ),
    )

    def export_to_excel(self, request, queryset):
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "JKUSOS Members"

        # Headers
        ws.append(['First Name', 'Last Name', 'Reg Number', 'Email'])

        # Data rows
        for user in queryset:
            ws.append([
                user.first_name,
                user.last_name,
                user.reg_number,
                user.email,
            ])

        # Save to BytesIO instead of deprecated save_virtual_workbook
        output = BytesIO()
        wb.save(output)
        output.seek(0)

        response = HttpResponse(
            output,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=JKUSOS_members.xlsx'
        return response
admin.site.register(User, UserAdmin)


@admin.register(MembershipPayment)
class MembershipPaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'transaction_code', 'amount', 'status', 'submitted_at')
    list_filter = ('status',)
    search_fields = ('user__email', 'transaction_code')
    actions = ['approve_selected', 'decline_selected']

    def approve_selected(self, request, queryset):
        updated = 0
        approved_now = []

        for payment in queryset:
            if payment.status != MembershipPayment.STATUS_APPROVED:
                payment.status = MembershipPayment.STATUS_APPROVED
                payment.save()
                approved_now.append(payment)
                updated += 1

        # After approving, re-check total approved amount for each user
        affected_users = set(payment.user for payment in approved_now)
        activated = 0
        for user in affected_users:
            total_approved = user.membershippayment_set.filter(
                status=MembershipPayment.STATUS_APPROVED
            ).aggregate(total=models.Sum('amount'))['total'] or 0

            if total_approved >= 300 and not user.is_member:
                user.is_member = True
                user.save()
                activated += 1

        self.message_user(
            request,
            f"{updated} payments approved. {activated} user(s) activated based on total approved payments ≥ KES 300."
        )

    approve_selected.short_description = "Approve selected membership payments"

    def decline_selected(self, request, queryset):
        updated = queryset.update(status=MembershipPayment.STATUS_DECLINED)
        self.message_user(request, f"{updated} payments marked as declined.")

    decline_selected.short_description = "Decline selected membership payments"


admin.site.register(PaymentSettings)


@admin.register(UserQuestion)
class UserQuestionAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'submitted_at', 'answered')
    list_filter = ('answered',)
    search_fields = ('user__email', 'question')



@admin.register(ContactSettings)
class ContactSettingsAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone', 'website','whatsapp_group','instagram')

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'submitted_at')
    search_fields = ('name', 'email', 'message')

@admin.register(ClubOfficial)
class ClubOfficialAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'email')
