from django.contrib.auth.models import User
from app.models import User, Restaurant, StandardHours, CustomHours, Booking, Review

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

# filepath: /Users/petervine/Developer/RestaBook/app/widgets.py
from django import forms
from django.utils.safestring import mark_safe

class StarRatingWidget(forms.Widget):
    def render(self, name, value, attrs=None, renderer=None):
        html = """
        <div class="star-rating">
            <input type="radio" name="{name}" value="1" {checked_1}> 1
            <input type="radio" name="{name}" value="2" {checked_2}> 2
            <input type="radio" name="{name}" value="3" {checked_3}> 3
            <input type="radio" name="{name}" value="4" {checked_4}> 4
            <input type="radio" name="{name}" value="5" {checked_5}> 5
        </div>
        """.format(
            name=name,
            checked_1='checked' if value == '1' else '',
            checked_2='checked' if value == '2' else '',
            checked_3='checked' if value == '3' else '',
            checked_4='checked' if value == '4' else '',
            checked_5='checked' if value == '5' else '',
        )
        return mark_safe(html)
    

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('star_rating', 'text')
        widgets = {
            'star_rating': StarRatingWidget(),
            'text': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }