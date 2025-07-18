# Generated by Django 5.2.3 on 2025-07-04 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_membershippayment_declined'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='membershippayment',
            name='approved',
        ),
        migrations.RemoveField(
            model_name='membershippayment',
            name='declined',
        ),
        migrations.AddField(
            model_name='membershippayment',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('declined', 'Declined')], default='pending', max_length=10),
        ),
    ]
