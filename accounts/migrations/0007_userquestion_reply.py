# Generated by Django 5.2.3 on 2025-07-04 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_userquestion'),
    ]

    operations = [
        migrations.AddField(
            model_name='userquestion',
            name='reply',
            field=models.TextField(blank=True, null=True),
        ),
    ]
