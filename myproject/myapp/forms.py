from dataclasses import field
from django import forms
from .models import Employee, Restaurant, MenuItem

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields=['name','role','contact','email','restaurant']
        
class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['name', 'address', 'total_tables', 'email']
        
class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['name', 'description', 'price']

