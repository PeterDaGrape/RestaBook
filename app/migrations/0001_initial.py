# Generated by Django 2.2.28 on 2025-03-12 11:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cuisine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=32)),
                ('cuisine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Cuisine')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255)),
                ('isManager', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='StandardHours',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_tables', models.IntegerField()),
                ('opening_time', models.TimeField()),
                ('closing_time', models.TimeField()),
                ('is_open', models.BooleanField()),
                ('week_day', models.IntegerField()),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Restaurant')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('star_rating', models.IntegerField()),
                ('text', models.CharField(max_length=255)),
                ('review_date', models.DateField()),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Restaurant')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.User')),
            ],
        ),
        migrations.AddField(
            model_name='restaurant',
            name='manager',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app.User'),
        ),
        migrations.CreateModel(
            name='CustomHours',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_tables', models.IntegerField()),
                ('is_open', models.BooleanField()),
                ('opening_time', models.TimeField()),
                ('closing_time', models.TimeField()),
                ('date', models.DateField()),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Restaurant')),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Restaurant')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.User')),
            ],
        ),
    ]
