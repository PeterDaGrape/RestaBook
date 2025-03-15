from django.db import models

from django.template.defaultfilters import slugify
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

class User(AbstractUser):
    
    isManager = models.BooleanField(default=False)


    def __str__(self):
        return self.username

class Cuisine(models.Model):

    name = models.CharField(max_length=32)
    def __str__(self):
        return self.name

class Restaurant(models.Model):
    cuisine = models.ForeignKey(Cuisine, on_delete=models.CASCADE)
    manager = models.OneToOneField(User, on_delete=models.CASCADE)

    slug = models.SlugField(unique=True)
    
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=32)
    
    max_capacity = models.IntegerField(default = 50)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Restaurant, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)


    date = models.DateField()
    time = models.TimeField()
    
    people_count = models.IntegerField(default=1)
    
    def save(self, *args, **kwargs):
        if self.people_count > 4:
            raise ValueError("A booking cannot exceed 4 people.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} booked at {self.restaurant.name} on {self.date} at {self.time}"
    


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    star_rating = models.IntegerField()
    text = models.CharField(max_length=255)

    review_date = models.DateField()

    def __str__(self):
        return self.user.username

class StandardHours(models.Model):  
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    number_tables = models.IntegerField()
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    is_open = models.BooleanField()
    week_day = models.IntegerField()

    def __str__(self):
        return self.restaurant + " " + str(self.week_day) + " " + str(self.is_open) 



class CustomHours(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    number_tables = models.IntegerField()
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    date = models.DateField()

    def __str__(self):

        return self.restaurant + " " + str(self.date) + " " + str(self.is_open) 