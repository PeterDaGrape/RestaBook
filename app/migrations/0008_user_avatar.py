# Generated by Django 2.2.28 on 2025-03-28 01:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_booking_is_completed'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='avatars/'),
        ),
    ]
