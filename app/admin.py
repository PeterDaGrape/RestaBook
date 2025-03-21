from django.contrib import admin

from app.models import User, Cuisine, Restaurant, Booking, Review, StandardHours, CustomHours

class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'manager', 'cuisine', 'email', 'address', 'phone')

admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(User)
admin.site.register(Cuisine)
admin.site.register(Booking)
admin.site.register(Review)
admin.site.register(StandardHours)
admin.site.register(CustomHours)
