"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from xml.dom.minidom import Document
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from myapp import views
from django.contrib.auth.views import LogoutView
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Admin Pages
    path('admin-panel/', views.admin_panel_view, name='admin_panel'),
    path('admin-panel/add-restaurant/', views.add_restaurant_view, name='add_restaurant'),
    path('admin-panel/restaurant-employees/', views.restaurant_employees_view, name='restaurant_employees'),
    path('admin-panel/view-all-restaurants/', views.view_all_restaurants_view, name='view_all_restaurants'),
    path('admin-panel/view-bookings/', views.view_bookings_view, name='view_bookings'),
    path('admin-panel/user-pages/', views.user_pages_view, name='user_pages'),
    path('admin-panel/edit-restaurant/<int:id>/', views.edit_restaurant_view, name='edit_restaurant'),
    path('admin-panel/delete-restaurant/<int:id>/', views.delete_restaurant_view, name='delete_restaurant'),
    
    # Employee Management
    path('manage_employees/', views.manage_employees, name='manage_employees'),
    path('delete_employee/<int:id>/', views.delete_employee, name='delete_employee'),
    path('admin-panel/edit-employee/<int:id>/', views.edit_employee, name='edit_employee'),
    path('admin-panel/delete-booking/<int:id>/',views.delete_booking_view,name='delete_booking'),
    path('signin/', views.login_view, name='signin'),
    path('logout/', views.logout_view, name='logout'),
    path('admin-panel/', views.admin_panel_view, name='admin_panel'),
    path('restaurant-login/', views.restaurant_login, name='restaurant_login'),
    path('restaurant-dashboard/', views.restaurant_dashboard, name='restaurant_dashboard'),
    path('add-menu-item/',views.add_menu_item, name='add_menu_item'),
    path('edit-menu/<int:item_id>/', views.edit_menu_item, name='edit_menu_item'),
    path('delete-menu/<int:item_id>/', views.delete_menu_item, name='delete_menu_item'),
    path('admin/view-menus/', views.view_all_menus, name='view_all_menus'),
    path('edit-tables/',views.edit_tables,name='edit_tables'),
    path('restaurant-logout',views.restaurant_logout,name='restaurant_logout'),
    path('', include('userapp.urls')),  # for frontend booking
    path('restaurant/', include('myapp.urls')), 
    
    
    #For userapp:
    path('',include('userapp.urls')),
    
    #for reports & analytics:
    path('admin-panel/reports/',views.reports_view,name='reports_view'),
] 

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


