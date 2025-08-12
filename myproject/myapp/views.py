from email import message
from email.headerregistry import Address
from email.mime import image
from multiprocessing import context
from django.shortcuts import render, redirect, get_object_or_404
from .models import Restaurant, Employee, Booking, MenuItem
from .forms import EmployeeForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from .forms import MenuItemForm
from django.utils import timezone
from django.db.models import Count,Sum
from datetime import timedelta
import io, base64
import matplotlib
matplotlib.use('Agg')   # non-interactive backend for servers
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')
from io import BytesIO





def admin_panel_view(request):
    restaurants = Restaurant.objects.all()
    total_tables = sum(r.total_tables for r in restaurants)
    total_bookings = Booking.objects.count()  #  count bookings
    all_restaurants = Restaurant.objects.all()
    bookings = Booking.objects.all().order_by('-booking_date','-booking_time')  #  get bookings
    return render(request, 'myapp/admin-panel.html', {
        'restaurants': restaurants,
        'total_tables': total_tables,
        'total_bookings': total_bookings,
        'all_restaurants': all_restaurants,
        'bookings': bookings, 
    })

def add_restaurant_view(request):
    if request.method == 'POST':
        # 1. Get data from submittted form
        name = request.POST.get('name')
        address = request.POST.get('address')
        total_tables = request.POST.get('total_tables')
        email = request.POST.get('email')
        image=request.FILES.get('image')

        # 2. Create a new user (restaurant head)
        password = "1234"  
        user = User.objects.create_user(username=email, email=email, password=password)

        # 3. Create restaurant and link it to this user using 'head'
        restaurant = Restaurant.objects.create(
            name=name,
            address=address,
            total_tables=total_tables,
            email=email,
            head=user, 
            image=image
        )

        # 4. Send email to the restaurant head with confirmation
        subject = 'Restaurant Added Successfully'
        message = f"""
Hello {name},

Your restaurant has been successfully added to our system.

Login Details:
Username: {email}
Password: {password}

You can now log in and manage your restaurant.

Details:
Name: {name}
Address: {address}
Total Tables: {total_tables}

Thank you!
"""
        send_mail(
            subject,
            message,
            'test@myresto.com',   # from
            [email],              # to
            fail_silently=False
        )

        # 5. Log this for admin (debug print)
        print(f"User created for restaurant {name} | Email: {email} | Password: {password}")

        # 6. Redirect to admin dashboard
        return redirect('admin_panel')

    # 7. Show form if GET request
    return render(request, 'myapp/add-restaurant.html')

def restaurant_employees_view(request):
    return render(request, 'myapp/restaurant-employees.html')

def view_all_restaurants_view(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'myapp/view-all-restaurants.html',{'restaurants': restaurants})

def view_bookings_view(request):
    bookings = Booking.objects.select_related('user').order_by('-date')
    return render(request, 'myapp/view-bookings.html', {'bookings': bookings})

def user_pages_view(request):
    return render(request, 'myapp/user-pages.html')

def edit_restaurant_view(request, id):
    restaurant = Restaurant.objects.get(id=id)
    
    if request.method == 'POST':
        restaurant.name = request.POST.get('name')
        restaurant.address = request.POST.get('address')
        restaurant.total_tables = request.POST.get('total_tables')
        restaurant.email = request.POST.get('email')
        
        
        # Handle image if uploaded
        if 'image' in request.FILES:
            restaurant.image = request.FILES['image']
        
        restaurant.save()
        return redirect('admin_panel')
    return render(request, 'myapp/edit-restaurant.html', {'restaurant':restaurant})

def delete_restaurant_view(request, id):
    restaurant = Restaurant.objects.get(id=id)
    restaurant.delete()
    return redirect('admin_panel')

def manage_employees(request):
    employees = Employee.objects.all()
    restaurants = Restaurant.objects.all()  

    if request.method == 'POST':
        name = request.POST.get('name')
        role = request.POST.get('role')
        contact = request.POST.get('contact')
        email=request.POST.get('email')
        restaurant_id = request.POST.get('restaurant')
        restaurant = Restaurant.objects.get(id=restaurant_id)

        Employee.objects.create(
            name=name,
            role=role,
            contact=contact,
            email=email,
            restaurant=restaurant
        )
        subject = 'Employee Added Successfully'
        message = f"""
Hello {name},

A big welcome to you from all of us in our restaurant.

Details:
Name: {name}
Your Role: {role}
Restaurant: {restaurant_id}

Thank you!
"""
        send_mail(
            subject,
            message,
            'test@myresto.com',    
            [email],               
            fail_silently=False
        )
        return redirect('manage_employees') 

    return render(request, 'myapp/restaurant-employees.html', {
        'employees': employees,
        'restaurants': restaurants  
    })

def delete_employee(request, id):
    emp = get_object_or_404(Employee, id=id)
    emp.delete()
    return redirect('manage_employees')  

def edit_employee(request, id):
    emp = get_object_or_404(Employee, id=id)
    restaurants = Restaurant.objects.all()

    if request.method == 'POST':
        emp.name = request.POST.get('name')
        emp.role = request.POST.get('role')
        emp.contact = request.POST.get('contact')
        emp.email = request.POST.get('email') 
        restaurant_id = request.POST.get('restaurant')
        emp.restaurant = get_object_or_404(Restaurant, id=restaurant_id)
        emp.save()
        return redirect('manage_employees')

    return render(request, 'myapp/edit-employee.html', {'emp': emp, 'restaurants': restaurants})

def delete_booking_view(request,id):
    booking = get_object_or_404(Booking, id=id)
    booking.delete()
    return redirect('admin_panel')

# Login View
def login_view(request):
    if request.method == 'POST':
        identifier = request.POST.get('username')  # This can be email or username
        password = request.POST.get('password')

        try:
            # 🔍 Get user by email (if email provided)
            if '@' in identifier:
                user = User.objects.get(email=identifier)
            else:
                user = User.objects.get(username=identifier)

            user = authenticate(request, username=user.username, password=password)

            if user is not None:
                login(request, user)

                #  Role-based Redirect
                if user.is_superuser:
                    return redirect('admin_panel')
                else:
                    return redirect('restaurant_dashboard')  # make sure this is defined

            else:
                messages.error(request, 'Invalid password.')

        except User.DoesNotExist:
            messages.error(request, 'User does not exist.')

    return render(request, 'signin.html')  # or signin.html

def logout_view(request):
    logout(request)
    return redirect('signin')

def restaurant_logout(request):
    logout(request)
    return redirect('signin')

@login_required
def restaurant_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            #  Get the user object using email
            user = User.objects.get(email=email)

            #  Authenticate using username, because Django needs username
            user = authenticate(request, username=user.username, password=password)

            if user is not None:
                login(request, user)
                return redirect('restaurant_dashboard')  
            else:
                messages.error(request, 'Invalid password.')
        
        except User.DoesNotExist:
            messages.error(request, 'User with this email does not exist.')

    return render(request, 'myapp/restaurant-login.html')

@login_required
def restaurant_dashboard(request):
    try:
        # Get the restaurant linked to the logged-in user
        restaurant = Restaurant.objects.get(head=request.user)

        # Only fetch data for that restaurant
        bookings = Booking.objects.filter(restaurant=restaurant)
        employees = Employee.objects.filter(restaurant=restaurant)
        menu_items = MenuItem.objects.filter(restaurant=restaurant)

        return render(request, 'myapp/restaurant-dashboard.html', {
            'restaurant': restaurant,
            'bookings': bookings,
            'employees': employees,
            'menu_items': menu_items
        })

    except Restaurant.DoesNotExist:
        return render(request, 'myapp/error.html', {'message': "No restaurant linked to this user."})

def add_menu_item(request):
    restaurant = Restaurant.objects.get(head=request.user)
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        price = request.POST['price']

        MenuItem.objects.create(
            restaurant=restaurant,
            name=name,
            description=description,
            price=price
        )
        return redirect('restaurant_dashboard')  
    return render(request, 'myapp/add-menu-item.html')

@login_required
def edit_tables(request):
    restaurant = Restaurant.objects.get(head=request.user)

    if request.method == 'POST':
        new_table_count = request.POST.get('tables')
        new_image = request.FILES.get('image')  

        if new_table_count:
            restaurant.total_tables = new_table_count

        if new_image:
            restaurant.image = new_image

        restaurant.save()
        messages.success(request, "Restaurant details updated.")
    
    return redirect('restaurant_dashboard')

@login_required
def edit_menu_item(request, item_id):
    restaurant = Restaurant.objects.get(head=request.user)
    item = get_object_or_404(MenuItem, id=item_id, restaurant=restaurant)

    if request.method == 'POST':
        form = MenuItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('restaurant_dashboard')
    else:
        form = MenuItemForm(instance=item)

    return render(request, 'myapp/edit-menu-item.html', {'form': form})

@login_required
def delete_menu_item(request, item_id):
    restaurant = Restaurant.objects.get(head=request.user)
    item = get_object_or_404(MenuItem, id=item_id, restaurant=restaurant)
    item.delete()
    return redirect('restaurant_dashboard')

@staff_member_required
def view_all_menus(request):
    menus = MenuItem.objects.select_related('restaurant').all()
    return render(request, 'myapp/admin-view-menus.html', {'menus': menus})



def reports_view(request):
    today = timezone.now().date()

    # Bookings per day
    daily_data = Booking.objects.values('booking_date').annotate(total=Count('id')).order_by('booking_date')
    dates = [str(d['booking_date']) for d in daily_data]
    counts = [d['total'] for d in daily_data]

    # Top restaurants
    rest_data = Booking.objects.values('restaurant__name').annotate(total=Count('id')).order_by('-total')[:5]
    rest_names = [r['restaurant__name'] for r in rest_data]
    rest_counts = [r['total'] for r in rest_data]

    # Revenue
    revenue_data = Booking.objects.values('restaurant__name').annotate(total_guests=Sum('guests'))
    revenue_labels = [r['restaurant__name'] for r in revenue_data]
    revenue_values = [(r['total_guests'] or 0) * 500 for r in revenue_data]

    # Guests histogram
    guests_list = list(Booking.objects.values_list('guests', flat=True))
    guest_bins = sorted(set(guests_list))
    guest_counts = [guests_list.count(g) for g in guest_bins]

    context = {
        "restaurants": [], #actual data
        "total_tables": 0,
        "total_bookings": Booking.objects.count(),
        "dates": dates,
        "counts": counts,
        "rest_names": rest_names,
        "rest_counts": rest_counts,
        "revenue_labels": revenue_labels,
        "revenue_values": revenue_values,
        "guest_bins": guest_bins,
        "guest_counts": guest_counts
    }
    return render(request, 'myapp/reports.html', context)

#  convertinggg matplotlib figure to base64 string
def fig_to_base64(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)


def get_chart_image():
    buffer = BytesIO() #create temporay file in memry
    plt.savefig(buffer, format='png', bbox_inches='tight') #chart of matplotlib save in png 
    buffer.seek(0) #file pointer to front for imh read
    image_png = buffer.getvalue()   #get wholw data of buffer in bytes 
    buffer.close() #memory cleanup
    graphic = base64.b64encode(image_png).decode('utf-8') #for direct use in html
    plt.close() 
    return graphic
