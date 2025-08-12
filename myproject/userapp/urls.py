from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('about/', views.about, name='about'),
    path('book/', views.book, name='book'),
    # path('menu/', views.menu, name='menu'),
    path('recipes/', views.recipes, name='recipes'),
    path('signin/', views.signin, name='signin'),
    path('restaurants/',views.restaurant_list,name='restaurant_list'),
    path('booking-success/', views.booking_success, name='booking_success'),
     path('user-booking/', views.user_booking_view, name='user_booking'),
    
    path('restaurant/<int:restaurant_id>/menu/', views.show_menu, name='show_menu'),
]

