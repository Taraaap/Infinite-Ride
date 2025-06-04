
from django.contrib import admin
from django.urls import path
from InfiniteRide import views
from django.contrib.auth import views as auth_views

from django.urls import re_path

urlpatterns = [
    path("",views.index, name="home"),
    path("about/",views.about, name="about"),
    path("vehicle/",views.vehicle_list, name="vehicle_list"),
    path("booking/",views.booking, name="booking"),
    path("contact/",views.contact, name="contact"),
    
    path("login/",views.user_login, name="login"),
    path("register/",views.register, name="register"),
    path("policy/",views.policy, name="policy"),
    
    path('reset_pass/', views.reset_pass, name='reset_pass'),
    path("verify_otp/", views.verify_otp, name="verify_otp"),
    path("save_password/", views.save_password, name="save_password"),

    path('forbidden_page/', views.forbidden_page, name='forbidden_page'),

    path('profile/', views.profile, name='profile'),  
    path('edit-profile/', views.edit_profile, name='edit_profile'), 
    
    path('logout/', views.logout_view, name='logout'),
    path('book/<str:vehicle_type>/<int:vehicle_id>',views.book_vehicle,name='book_vehicle'),
    path('create-booking/', views.create_booking, name='create_booking'),
    path('booking-history/', views.booking_history, name='booking_history'),
    path('bill/<int:booking_id>/', views.bill_detail, name='bill_detail'),
    path("submit-review/", views.submit_review, name="submit_review"),
    path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),



    re_path(r'^(?!about|vehicle|booking|contact|login|register|policy|reset_pass|verify_otp|save_password|profile|edit-profile|logout|submit-review|admin/admin-login|admin/admin-logout|admin/dashboard|admin/admin-contact|admin/admin-review|admin/user|admin/bike|admin/bikes|admin/car|admin/large_vehicle|admin/large_vehicles|admin/admin_booking|admin/bookings|admin/admin_bill|admin/bills|admin_reset_pass|admin_verify_otp|admin_save_password|).*$', views.forbidden_page),
]
