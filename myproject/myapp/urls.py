from django.conf import settings
from django.urls import path
from . import views

urlpatterns = [
    path('admin-panel/', views.admin_panel_view, name='admin_panel'),
    path('restaurant-dashboard/', views.restaurant_dashboard, name='restaurant_dashboard'),

] 