from django.contrib.auth.models import User
from app.models import User, Booking 
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
        
        
class BookingForm(forms.ModelForm):
    name = forms.CharField(label="Your Name", max_length=100, required=True)
    email = forms.EmailField(label="Your Email", required=True)

    class Meta: 
        model = Booking 
        fields = ['name', 'email', 'date', 'time', 'people_count']

    def clean_people_count(self):
        people_count = self.cleaned_data.get('people_count')
        if people_count > 4:
            raise forms.ValidationError("You can't book a reservation for more than 4 people.")
        return people_count