from email.mime import image
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    total_tables = models.IntegerField()
    email = models.EmailField(default='test@example.com')
    head = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    contact=models.CharField(max_length=20,blank=True)
    staus=models.CharField(max_length=20,default="Open")
    image=models.ImageField(upload_to='restaurant_images/',null=True,blank=True)
    service_options=models.TextField(blank=True,help_text="e.g. All you can Eat . Outdoor seating . Vegan options")

    def _str_(self):
        return self.name
    
class MenuItem(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def _str_(self):
        return self.name
    
class Employee(models.Model):
    name=models.CharField(max_length=100)
    role= models.CharField(max_length=50)
    contact=models.CharField(max_length=50)
    email = models.EmailField(default='test@example.com')
    restaurant=models.ForeignKey(Restaurant,on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.name}({self.role})"
    

class Booking(models.Model):
    customer_name = models.CharField(max_length=100)
    contact = models.CharField(max_length=20)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    booking_date = models.DateField()
    booking_time = models.TimeField()
    guests = models.IntegerField(default=0)
    email = models.EmailField(default='test@example.com')
    def __str__(self):
        return f"{self.customer_name} - {self.restaurant.name} on {self.booking_date}"

    