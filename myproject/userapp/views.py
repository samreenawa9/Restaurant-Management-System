from django.shortcuts import render, get_object_or_404
from myapp.models import Restaurant, MenuItem, Booking
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings

def home(request):
    restaurants=Restaurant.objects.all()
    return render(request,'index.html',{'restaurants':restaurants})

def about(request):
    return render(request,'about.html')

def book(request):
    restaurants = Restaurant.objects.all()
    if request.method == 'POST':
        customer_name = request.POST.get('customer_name')
        email = request.POST.get('email')  # user ka email
        contact = request.POST.get('contact')
        restaurant_id = request.POST.get('restaurant')
        booking_date = request.POST.get('booking_date')
        booking_time = request.POST.get('booking_time')
        guests = request.POST.get('guests')

        # Get restaurant
        restaurant = Restaurant.objects.get(id=restaurant_id)

        # Save booking in DB
        Booking.objects.create(
            customer_name=customer_name,
            email=email,
            contact=contact,
            restaurant=restaurant,
            booking_date=booking_date,
            booking_time=booking_time,
            guests=guests
        )

        # Email to User only
        subject_user = "Your Table Booking Confirmation"
        message_user = f"""
Dear {customer_name},

Your booking at your favourite restaurant: {restaurant.name} is confirmed.

Date: {booking_date}
Time: {booking_time}
Guests: {guests}

We look forward to serving you!

Thank you,
From, {restaurant.name}
"""
        send_mail(subject_user, message_user, settings.EMAIL_HOST_USER, [email], fail_silently=False)

        # Show success page
        return render(request, 'booking-success.html', {'name': customer_name})

    return render(request, 'book.html', {'restaurants': restaurants})


def booking_success(request):
    return render(request, 'booking-success.html')

def user_booking_view(request):
    # your logic
    return render(request, 'user_booking.html')


# def menu(request):
#     return render(request,'menu.html')

def recipes(request):
    return render(request,'recipes.html')

def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('admin_panel')  # name from myapp.urls
            else:
                return redirect('restaurant_dashboard')  # name from myapp.urls
        else:
            messages.error(request, 'Invalid username or password')
            return render(request, 'signin.html')

    return render(request, 'signin.html')

def restaurant_list(request):
    restaurants=Restaurant.objects.all()
    return render(request,'restaurant_list.html',{'restaurants':restaurants})

def show_menu(request, restaurant_id):
    # Getting the restaurant object
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)

    # Getting menu items related to this restaurant
    menu_items = MenuItem.objects.filter(restaurant=restaurant)

    # Passing to template
    return render(request, 'menu.html', {
        'restaurant': restaurant,
        'menu_items': menu_items
    })