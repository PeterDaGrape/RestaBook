from django.contrib.auth.models import User
from app.models import User, Restaurant, StandardHours, CustomHours, Booking

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
        fields = ('number_tables', 'opening_time', 'closing_time', 'week_day')
        widgets = {
            'opening_time': forms.TimeInput(attrs={'type': 'time'}),
            'closing_time': forms.TimeInput(attrs={'type': 'time'}),
        }

class CustomHoursForm(forms.ModelForm):
    class Meta:
        model = CustomHours
        fields = ('number_tables', 'opening_time', 'closing_time', 'date')
        widgets = {
            'opening_time': forms.TimeInput(attrs={'type': 'time'}),
            'closing_time': forms.TimeInput(attrs={'type': 'time'}),
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class BookingForm(forms.ModelForm):
    name = forms.CharField(label="Your Name", max_length=100, required=True)
    email = forms.EmailField(label="Your Email", required=True)

    class Meta: 
        model = Booking 
        fields = ['name', 'email', 'date', 'time']

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ('date', 'time')
        widgets = {
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'date': forms.DateInput(attrs={'type': 'date'}),
        }