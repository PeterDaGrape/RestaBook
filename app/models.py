from django.db import models

from django.template.defaultfilters import slugify
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    isManager = models.BooleanField(default=False)


    def __str__(self):
        return self.username

class Cuisine(models.Model):

    name = models.CharField(max_length=32)
    def __str__(self):
        return self.name
    
    def get_instance(name):
        return Cuisine.objects.get_or_create(name=name)[0]

class Restaurant(models.Model):
    cuisine = models.ForeignKey(Cuisine, on_delete=models.CASCADE)
    manager = models.OneToOneField(User, on_delete=models.CASCADE)

    slug = models.SlugField(unique=True)
    
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=32)
    city = models.CharField(max_length=100)

    bookings_allowed = models.BooleanField(default=True)


    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Restaurant, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    def calculate_average_stars(self):
        
        reviews = Review.objects.filter(restaurant = self)
        if not reviews:
            return 0 
         

        total = 0
        i = 0
        for i in range(len(reviews)):
            review_stars = reviews[i].star_rating
            if review_stars >= 0 and review_stars <= 5:
                total += review_stars
        average = total / (i+1)
        return round(average, 1)
        

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    date = models.DateField()
    time = models.TimeField()

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
    DAYS_OF_WEEK = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]
    number_tables = models.IntegerField()
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    week_day = models.CharField(max_length=9, choices=DAYS_OF_WEEK)
    
    bookings_allowed = models.BooleanField(default=True)
    class Meta:
        unique_together = ('restaurant', 'week_day')  # Prevent duplicate hours for the same day per restaurant

    def __str__(self):
        return str(self.opening_time) + " - " + str(self.closing_time) + " " + str(self.week_day)



class CustomHours(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    number_tables = models.IntegerField()
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    date = models.DateField()
    bookings_allowed = models.BooleanField(default=True)

    class Meta:
        unique_together = ('restaurant', 'date')  # Prevent duplicate hours for the same date per restaurant

    def __str__(self):

        return str(self.opening_time) + " - " + str(self.closing_time) + " " + str(self.date)
