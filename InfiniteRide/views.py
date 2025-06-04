import re
from django.shortcuts import render, HttpResponse , redirect,get_object_or_404
from datetime import datetime
from InfiniteRide.models import Contact
from django.contrib import messages
# from django.contrib.auth.models import User
from InfiniteRide.models import CustomUser
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from .models import Vehicle
from .models import Booking, Car, Bike, LargeVehicle ,Review,Bill
from datetime import date
from django.utils import timezone
from django.template.loader import render_to_string
import random
import string
import re

# Create your views here.
def index(request):
    featured_bikes = Bike.objects.filter(featured_vehicle=True)  
    featured_cars = Car.objects.filter(featured_vehicle=True)  
    featured_large_vehicles = LargeVehicle.objects.filter(featured_vehicle=True)  

    return render(request, 'index.html', {
        'featured_bikes': featured_bikes,
        'featured_cars': featured_cars,
        'featured_large_vehicles': featured_large_vehicles
    })

def about(request):
    return render(request, 'about.html')

def vehicle(request):
    return render(request, 'vehicle.html')

def booking(request):
    return render(request, 'booking.html')

def invoice_detail(request):
    return render(request, 'invoice.html')


# Contact
def contact(request):
    if request.method =="POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        
        name_regex = r'^[A-Za-z ]{2,50}$'
        if not re.match(name_regex, name):
            messages.error(request, "Name can only contain letters ")
            return render(request, 'contact.html', {'name': name, 'email': email, 'phone': phone})
        
        phone_regex = r'^9\d{9}$'
        if not re.match(phone_regex, phone):
            messages.error(request, "Enter a 10-digit  number starting with 9.")
            return render(request, 'contact.html', {'name': name, 'email': email, 'phone': phone})
        
        
        contact= Contact(name=name,email=email,phone=phone,message=message,
        date=datetime.today())
        contact.save()
        messages.success(request, "sent")
    return render(request, 'contact.html')



# LogIn
def user_login(request):
    
   if request.method=="POST":
       email=request.POST['email']
       password=request.POST['password']
       
       user=authenticate(request, username=email,password=password)
       if user is not None: 
           
           if user.is_superuser or user.is_staff:
                messages.error(request, "Invalid Credentials")
                return redirect('login')
            
           auth_login(request, user)
           return redirect('home')
       else:
           messages.error(request,"Invalid Credentials")
           
   
   return render(request, 'login.html')

# SignUp

def register(request):
    if request.method=="POST":
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        password=request.POST['password']
        confirmpassword=request.POST['confirmpassword']
        
        
        name_regex = r'^[A-Za-z ]{2,50}$'
        if not re.match(name_regex, name):
            messages.error(request, "Name can only contain letters ")
            return render(request, 'register.html', {'name': name, 'email': email, 'phone': phone})
        
        if CustomUser.objects.filter(email=email).first():
            messages.error(request, "Email already taken.")
            return render(request, 'register.html', {'name': name, 'email': email, 'phone': phone})
        
        if CustomUser.objects.filter(phone=phone).exists():
            messages.error(request, "Phone number is already taken.")
            return render(request, 'register.html', {'name': name, 'email': email, 'phone': phone})
         
        
        phone_regex = r'^9\d{9}$'
        if not re.match(phone_regex, phone):
            messages.error(request, "Enter a 10-digit  number starting with 9.")
            return render(request, 'register.html', {'name': name, 'email': email, 'phone': phone})
        
        # Password Validation
        PASSWORD_REGEX = r'^(?=.*\d).{8,}$'  
        if not re.match(PASSWORD_REGEX, password):
            messages.error(request, "Password must be at least 8 characters long and contain at least")
            return render(request, 'register.html', {'name': name, 'email': email, 'phone': phone})

        elif password != confirmpassword:
            messages.error(request, "Password and confirm password do not match.")
            return render(request, 'register.html', {'name': name, 'email': email, 'phone': phone})
        
        user = CustomUser.objects.create_user(
        username=name,
        email=email,phone=phone,
        password=password)
        user.first_name=name
        user.save()
        messages.success(request, "Your account hasbeen successfully created")
        return redirect('login')
        
    return render(request, 'register.html')


# policy
def policy(request):
    return render(request, 'policy.html')

# View for user profile page
@login_required
def profile(request):
    # You can fetch the user's data here if needed
    return render(request, 'profile.html', 
                  {'user': request.user})

# View for editing profile
@login_required
def edit_profile(request):
    if request.method == "POST":
        user = request.user 

        # Get form data
        name = request.POST.get("name").strip()
        email = request.POST.get("email").strip()
        phone = request.POST.get("phone").strip()
        current_password = request.POST.get("current_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if not current_password:
            messages.error(request, "Please enter your current password to save changes.")
            return render(request, 'edit_profile.html', { "user": user })

# Check if the current password is correct
        if not user.check_password(current_password):
            messages.error(request, "Current password is incorrect.")
            return render(request, 'edit_profile.html', { "user": user })

        # Validate name
        if not re.match(r'^[A-Za-z ]{2,50}$', name):
           messages.error(request, "Name can only contain letters and spaces.")
           return render(request, 'edit_profile.html', { "user": user })

        # Email validation
        if CustomUser.objects.filter(email=email).exclude(id=user.id).exists():
            messages.error(request, "Email is already taken.")
            return render(request, 'edit_profile.html', { "user": user })

        # Phone validation
        if not re.match(r'^9\d{9}$', phone):
            messages.error(request, "Enter a 10-digit phone number starting with 9.")
            return render(request, 'edit_profile.html', { "user": user })

        if CustomUser.objects.filter(phone=phone).exclude(id=user.id).exists():
            messages.error(request, "Phone number is already taken.")
            return render(request, 'edit_profile.html', { "user": user })

        # Password validation
        if new_password or confirm_password:
            if not re.match(r'^.{8,}$', new_password):
                messages.error(request, "New password must be at least 8 characters.")
                return render(request, 'edit_profile.html', { "user": user })
            if new_password != confirm_password:
                messages.error(request, "New password and confirm password do not match.")
                return render(request, 'edit_profile.html', { "user": user })
            user.set_password(new_password)
            update_session_auth_hash(request, user)

        # Update user details
        user.username = name
        user.email = email
        user.phone = phone
        user.save()

        # Provide success message and redirect
        messages.success(request, "Profile updated successfully!")
        return redirect("profile")

    return render(request, 'edit_profile.html')

def booking_history(request):
    bookings = Booking.objects.filter(user=request.user)
    for booking in bookings:
        booking.has_review = booking.reviews.exists()
    if request.method == "POST":
        review_text = request.POST.get("review_text")
        booking_id = request.POST.get("booking_id")
        
        booking = get_object_or_404(Booking, id=booking_id)
        
        if not booking.reviews.exists():
            Review.objects.create(
                booking=booking,
                user=request.user,
                review_text=review_text
            )
            messages.success(request, "Review submitted successfully!")
        else:
            messages.error(request, "You have already submitted a review for this booking.")
        
        return redirect('booking_history')  # Use the name of your URL pattern

    return render(request, 'booking_history.html', {'bookings': bookings})

# View for logout
def logout_view(request):
    logout(request)
    return redirect('home') 

def vehicle_list(request):
    cars = Car.objects.all().order_by('-available')
    bikes = Bike.objects.all().order_by('-available')
    large_vehicles = LargeVehicle.objects.all().order_by('-available')

   
    return render(request, 'vehicle_list.html', {
        'cars': cars,
        'bikes': bikes,
        'large_vehicles': large_vehicles
    })

def book_vehicle(request, vehicle_type, vehicle_id):
    vehicle = None
    if vehicle_type == 'car':
        vehicle = get_object_or_404(Car, id=vehicle_id)
    elif vehicle_type == 'bike':
        vehicle = get_object_or_404(Bike, id=vehicle_id)
    elif vehicle_type == 'large_vehicle':
        vehicle = get_object_or_404(LargeVehicle, id=vehicle_id)
    else:
        return HttpResponse("Invalid vehicle type", status=400)

    return render(request, 'booking.html', {'vehicle': vehicle, 'vehicle_type': vehicle_type})


ALLOWED_EXTENSIONS = ['.pdf', '.png', '.jpg', '.jpeg']
import os
@login_required
def create_booking(request):
   
    if request.method == 'POST':
        vehicle_id = request.POST.get('vehicle')
        vehicle_type = request.POST.get('vehicle_type')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        self_drive = request.POST.get('self_drive', 'off') == 'on'  
        license_upload = request.FILES.get('license')  
        dropoff = request.POST.get('dropoff', 'off') == 'on' 
        dropoff_address = request.POST.get('dropoff_address', '').strip() 
        special_requirements = request.POST.get('special_requirements', '').strip()

        if license_upload:
            ext = os.path.splitext(license_upload.name)[1].lower()
            if ext not in ALLOWED_EXTENSIONS:
                messages.error(request, "Invalid file type for license. Only PDF, PNG, JPG, or JPEG allowed.")
                return redirect('booking')
            
        if not start_date or not end_date:
            messages.error(request, "Please select start and end dates.")
            # return redirect('booking')

        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        except ValueError:
            messages.error(request, "Invalid date format.")
            return redirect('booking')

        vehicle_model = {'car': Car, 'bike': Bike, 'large_vehicle': LargeVehicle}.get(vehicle_type)
        if not vehicle_model:
            messages.error(request, "Invalid vehicle type.")
            return redirect('booking')
        
        vehicle = get_object_or_404(vehicle_model, id=vehicle_id)

        vehicle = get_object_or_404(vehicle_model, id=vehicle_id)
        total_days = (end_date - start_date).days + 1  
        total_amount = total_days * vehicle.price_per_day
 
        user_phone = request.user.phone if hasattr(request.user, 'phone') else ''
        # Create the booking
        booking = Booking.objects.create(
            user=request.user,
            phone_number=user_phone,
            start_date=start_date,
            end_date=end_date,
            car=vehicle if vehicle_type == 'car' else None,
            bike=vehicle if vehicle_type == 'bike' else None,
            large_vehicle=vehicle if vehicle_type == 'large_vehicle' else None,
            total_days=total_days,
            total_amount=total_amount,
            status='pending',
            self_drive=self_drive,
            license_document=license_upload,
            drop_off_required=dropoff,
            drop_off_address=dropoff_address,
            special_requirements=special_requirements
        )
        messages.success(request, "Your booking has been successfully created!")
        return redirect('home')
        

    return render(request, 'vehicle.html')


@login_required
def confirm_booking(request, booking_id):
    """Confirms a booking and updates its status."""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if request.method == 'POST':
        booking.status = 'confirmed'
        booking.save()

        
        

        messages.success(request, "Your booking has been confirmed and an invoice has been generated!")
        return redirect('booking_history')  
    return render(request, 'vehicle.html', {'booking': booking})

def booking_history(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-start_date')
    return render(request, 'Booking_history.html', {'bookings': bookings})


def bill_detail(request, booking_id):
    try:
        booking = Booking.objects.get(id=booking_id)
    except Booking.DoesNotExist:
        return render(request, 'error.html', {'message': 'Booking not found'})

    return render(request, 'bill.html', {'booking': booking})
      
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
@login_required  
@csrf_exempt  
def update_payment_status(request, booking_id):
    if not request.user.is_superuser: 
        return JsonResponse({"success": False, "error": "Unauthorized"}, status=403)

    booking = get_object_or_404(Booking, id=booking_id)

    if request.method == "POST":
        data = json.loads(request.body) 
        new_status = data.get("status", "Unpaid")
        booking.payment_status = new_status
        booking.save()  
        return JsonResponse({"success": True, "new_status": new_status})  

    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)

@login_required
def submit_review(request):
    if request.method == "POST":
        booking_id = request.POST.get("booking_id")
        review_text = request.POST.get("review_text")

        booking = get_object_or_404(Booking, id=booking_id)

       
        if booking.user != request.user:
            return redirect("booking_history") 

        if booking.reviews.exists():
            return redirect("booking_history")  

        
        Review.objects.create(
            booking=booking,
            user=request.user,
            review_text=review_text
        )
        
        messages.success(request, "Your review has been submitted successfully!")
        return redirect("booking_history")  

    return redirect("booking_history")


from django.core.mail import send_mail
def reset_pass(request):
    if request.method == "POST":
        email = request.POST.get("email")

        user = CustomUser.objects.filter(email=email).first()

        if user:
            if user.is_superuser or user.is_staff:
                messages.error(request, "Invalid Email.")
                return render(request, 'reset_pass.html')
            
            otp = f"{random.randint(100000, 999999)}"  
            print(f"Generated OTP: {otp}")

            request.session["reset_email"] = email
            request.session["reset_otp"] = otp

            send_mail(
                "Password Reset OTP",
                f"Your OTP for password reset is: {otp}",
                "no-reply@yourdomain.com",
                [email],
                fail_silently=False,
            )

            return redirect("verify_otp")
        else:
            messages.error(request, "Invalid Email")
    

    return render(request, 'reset_pass.html')


def verify_otp(request):
    otp_verified = False
    if request.method == "POST":
        entered_otp = request.POST.get("otp")
        stored_otp = request.session.get("reset_otp")
        
        if stored_otp and str(stored_otp) == entered_otp:
            otp_verified = True
            return render(request, "verify_otp.html", {"otp_verified": True})
        else:
            messages.error(request, "Invalid OTP. Please try again.")
            return redirect("verify_otp")

    return render(request, "verify_otp.html",{"otp_verified": otp_verified})

from django.contrib.auth.hashers import make_password

def save_password(request):
    if request.method == "POST":
        email = request.session.get("reset_email")
        user = CustomUser.objects.filter(email=email).first()

        if user.is_superuser or user.is_staff:
            messages.error(request, "Admin users cannot reset passwords here.")
            return redirect("verify_otp")

        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        # Password validation
        PASSWORD_REGEX = r'^.{8,}$'  # Password must be at least 8 characters long
        if not re.match(PASSWORD_REGEX, new_password):
            messages.error(request, "Password must be at least 8 characters long.")
            return redirect("verify_otp")
        
        if new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("verify_otp")

        user.password = make_password(new_password)
        user.save()

        messages.success(request, "Password successfully reset. Please log in.")
        return redirect("login")

    return redirect("verify_otp")

def forbidden_page(request):
    return render(request, 'forbidden_page.html')

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if booking.status != 'Canceled' and not booking.is_completed:
        booking.status = 'Canceled'
        booking.save()
        messages.success(request, 'Your booking has been canceled successfully.')
    else:
        messages.warning(request, 'Booking cannot be canceled.')

    return redirect('booking_history')
