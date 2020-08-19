from django.db import models

# Create your models here.

class ContactPG(models.Model):
	Name = models.CharField(max_length=100)
	Email = models.EmailField(max_length=100)
	Subject = models.CharField(max_length=100)
	Message = models.CharField(max_length=300)
	Status = models.CharField(max_length=100)

RENT_CHOICES = [ 
('daily', 'Daily'),
('monthly', 'Monthly'),
('quarterly', 'Quarterly'),
('Yearly', 'Yearly'),
]
ROOM_CHOICES = [
('singleroom', 'Singleroom'),
('twosharedroom', 'Twosharedroom'),
('threesharedroom', 'Threesharedroom'),
('foursharedroom', 'Foursharedroom'),
]
MEALS = [
('onetime', 'Breakfast only'),
('twotimes', 'Breakfast & Dinner'),
('threetimes', 'Breakfast, Lunch & Dinner'),
] 
LOCATION = [
('uk', 'United Kingdom'),
('australia', 'Australia'),
('canada', 'Canada'),
('germany', 'Germany'),
] 
class FindPG(models.Model):
  pgname = models.CharField(max_length=100,default='Stella Dimora')
  pgaddress = models.CharField(max_length=100,default='Stella Dimora,United Kingdom')
  rentchoice = models.CharField(max_length=100, choices=RENT_CHOICES, default='monthly')
  roomchoice = models.CharField(max_length=100, choices=ROOM_CHOICES, default='singleroom')
  mealchoice = models.CharField(max_length=100, choices=MEALS, default='threetimes')
  location = models.CharField(max_length=100, choices=LOCATION, default='australia')
  contactno = models.CharField(max_length=12,default='null')

class Notifications(models.Model):
  pgname = models.CharField(max_length=100,default='Stella Dimora')
  username = models.CharField(max_length=100,default="Parvathy")
  notif_msg = models.CharField(max_length=200,default='Viewed your conatct information')