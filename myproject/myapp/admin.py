from django.contrib import admin
from .models import Restaurant ,Employee, Booking

# Register your models here.


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display=['name','email','staus','contact']
    fields=['name','address','total_tables','email','head','contact','staus','image','service_options']
admin.site.register(Employee)
admin.site.register(Booking)