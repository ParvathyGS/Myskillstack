from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserForm(forms.Form):
	# Username = forms.CharField(label="User Name",(attrs={}))
	Username = forms.CharField(label="User Name")
	EmailId = forms.EmailField(max_length=200, help_text='Required')
	Password = forms.CharField(widget=forms.PasswordInput(),label="Password")
	Confirm_Password = forms.CharField(widget=forms.PasswordInput(),label = "Confirm Password")

class LoginForm(forms.Form):
	username = forms.CharField(widget=forms.TextInput())
	password = forms.CharField(widget=forms.PasswordInput())

class ContactPg(forms.Form):
	Name = forms.CharField(widget=forms.TextInput())
	Email = forms.EmailField(max_length=200, help_text='Required')
	Subject = forms.CharField(widget=forms.TextInput())
	Message = forms.CharField(widget=forms.TextInput())


RENT_CHOICES = [ 
('daily', 'Daily Rent Plan'),
('monthly', 'Monthly Rent Plan'),
('quarterly', 'Quarterly Rent Plan'),
('Yearly', 'Yearly Rent Plan'),
]
ROOM_CHOICES = [
('Singleroom', 'Singleroom'),
('Twosharedroom', 'Twosharedroom'),
('Threesharedroom', 'Threesharedroom'),
('Foursharedroom', 'Foursharedroom'),
]
MEALS = [
('Breakfast only', 'Breakfast only'),
('Breakfast & Dinner', 'Breakfast & Dinner'),
('Breakfast, Lunch & Dinner', 'Breakfast, Lunch & Dinner'),
] 
LOCATION = [
('UK', 'United Kingdom'),
('Australia', 'Australia'),
('Canada', 'Canada'),
('Germany', 'Germany'),
] 
class FindPg(forms.Form):
	Pgname = forms.CharField(max_length=100)
	Pgaddress = forms.CharField(max_length=100)
	Rentplan  = forms.CharField(max_length=100,label='Rent Plan', widget=forms.Select(choices=RENT_CHOICES))
	Roomtype = forms.CharField(max_length=100,label='Room Type', widget=forms.Select(choices=ROOM_CHOICES))
	Mealplan = forms.CharField(max_length=100,label='Meal Plan', widget=forms.Select(choices=MEALS))
	Location = forms.CharField(max_length=100,label='Location', widget=forms.Select(choices=LOCATION))
	ContactNo = forms.CharField(max_length=12)

class Changepswd(forms.Form):
	username = forms.CharField(max_length=100)
	EmailId = forms.EmailField(max_length=200, help_text='Required')
	newPassword = forms.CharField(widget=forms.PasswordInput(),label="New Password")
	confirmPassword = forms.CharField(widget=forms.PasswordInput(),label = "Confirm Password")
	