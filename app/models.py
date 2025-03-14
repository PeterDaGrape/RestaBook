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
    
    def clean (self):
        if self.people_count > 4:
            raise ValidationError("A booking cannot have more than 4 people")
        
        # Check if the total number of bookings at the restaurant exceeds the max capacity
        bookings_at_time = Booking.objects.filter(restaurant=self.restaurant, date=self.date, time=self.time)
        total_people_at_time = sum(booking.people_count for booking in bookings_at_time)
        
        if total_people_at_time + self.people_count > self.restaurant.max_capacity:
            raise ValidationError(f"The restaurant's capacity is exceeded for this time. Max capacity is {self.restaurant.max_capacity}.")

    def __str__(self):
        return self.user.username + " " + str(self.date) + " " + str(self.time)
    


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
    is_open = models.BooleanField()
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    date = models.DateField()

    def __str__(self):

        return self.restaurant + " " + str(self.date) + " " + str(self.is_open) 