from django.contrib.auth.models import User
from app.models import User, Restaurant, StandardHours
from django import forms


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'password',)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ()


class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ('name', 'email', 'address', 'phone', 'cuisine')



class StandardHoursForm(forms.ModelForm):
    class Meta:
        model = StandardHours
        fields = ('number_tables', 'opening_time', 'closing_time', 'is_open', 'week_day')