from django.db import models

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    isManager = models.BooleanField()

class Cuisine(models.Model):

    name = models.CharField(max_length=32)

class Restaurant(models.Model):
    cuisine = models.ForeignKey(Cuisine, on_delete=models.CASCADE)
    manager = models.OneToOneField(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=32)


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    date = models.DateField()
    time = models.TimeField()

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    star_rating = models.IntegerField()
    text = models.CharField()

    review_date = models.DateField()

class StandardHours(models.Model):  
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    number_tables = models.IntegerField()
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    is_open = models.BooleanField()
    week_day = models.IntegerField()


class CustomHours(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    number_tables = models.IntegerField()
    is_open = models.BooleanField()
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    date = models.DateField()