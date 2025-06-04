from django.urls import path
from admin_panel import views

urlpatterns = [
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-logout/', views.admin_logout, name='admin_logout'),
    path('dashboard/', views.admin_dashboard, name='dashboard'),
    path('admin-contact/', views.admin_contact, name='admin_contact'),
    path('admin-review/', views.admin_review, name='admin_review'),
    
    path('user/', views.admin_user_list, name='user'),
    path('users/add/', views.add_user, name='add_user'),
    path('users/edit/<int:user_id>/', views.edit_user, name='user_details'),
    path('users/delete/<int:user_id>/', views.delete_user, name='delete_user'),
    
    
    
    path('bike/', views.admin_bike, name='bike'),
    path('bikes/add/', views.add_bike, name='add_bike'),
    path('bikes/edit/<int:bike_id>/', views.edit_bike, name='bike_details'),
    path('bikes/delete/<int:bike_id>/', views.delete_bike, name='delete_bike'),
    
    path('car/', views.admin_car, name='car'),
    path('cars/add/', views.add_car, name='add_car'),
    path('cars/edit/<int:car_id>/', views.edit_car, name='car_details'),
    path('cars/delete/<int:car_id>/', views.delete_car, name='delete_car'),
    
    path('large_vehicle/', views.admin_large_vehicle, name='large_vehicle'),
    path('large_vehicles/add/', views.add_large_vehicle, name='add_large_vehicle'),
    path('large_vehicles/edit/<int:large_vehicle_id>/', views.edit_large_vehicle, name='large_vehicle_details'),
    path('large_vehicles/delete/<int:large_vehicle_id>/', views.delete_large_vehicle, name='delete_large_vehicle'),
    
    path('admin_booking/', views.admin_booking, name='admin_booking'),
    path('bookings/add/', views.add_booking, name='add_booking'),
    path('bookings/edit/<int:booking_id>/', views.edit_booking, name='booking_details'),
    path('bookings/delete/<int:booking_id>/', views.delete_booking, name='delete_booking'),
    
    path('admin_bill/', views.admin_bill, name='admin_bill'),
    path('bills/add/', views.add_bill, name='add_bill'),
    path('bills/edit/<int:bill_id>/', views.edit_bill, name='bill_details'),
    path('bills/delete/<int:bill_id>/', views.delete_bill, name='delete_bill'),
    
    
    
    path('admin_reset_pass/', views.admin_reset_pass, name='admin_reset_pass'),
    path("admin_verify_otp/", views.admin_verify_otp, name="admin_verify_otp"),
    path("admin_save_password/", views.admin_save_password, name="admin_save_password"),
    
    ]
