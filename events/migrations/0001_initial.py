# Generated by Django 5.2.3 on 2025-07-01 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('date', models.DateTimeField()),
                ('type', models.CharField(choices=[('trip', 'Academic Trip'), ('game', 'Game Night'), ('workshop', 'Workshop'), ('conference', 'Conference'), ('other', 'Other')], max_length=20)),
                ('location', models.CharField(blank=True, max_length=200, null=True)),
                ('banner', models.ImageField(blank=True, null=True, upload_to='event_banners/')),
                ('registration_required', models.BooleanField(default=False)),
                ('payment_required', models.BooleanField(default=False)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
            ],
        ),
    ]
