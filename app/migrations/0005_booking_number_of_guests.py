# Generated by Django 2.2.28 on 2025-03-27 23:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20250326_1932'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='number_of_guests',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
