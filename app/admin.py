from django.contrib import admin

from app.models import User, Cuisine, Restaurant, Booking, Review, StandardHours, CustomHours

admin.site.register(User)
admin.site.register(Cuisine)
admin.site.register(Restaurant)
admin.site.register(Booking)
admin.site.register(Review)
admin.site.register(StandardHours)
admin.site.register(CustomHours)
