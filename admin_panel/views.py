from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.decorators import user_passes_test
from InfiniteRide.models import *
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseBadRequest
from django.contrib.admin.views.decorators import staff_member_required
import re




def admin_login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        
        user = authenticate(request, username=email, password=password)
        
        if user is not None and (user.is_superuser or user.is_staff ): 
            auth_login(request, user)
            return redirect('dashboard') 
    
        else:
            messages.error(request, "Invalid admin credentials")
            return redirect('admin_login') 
         
       
    return render(request, 'admin_login.html') 
def admin_logout(request):
    logout(request)
    return redirect('admin_login')

@user_passes_test(lambda u: u.is_superuser or u.is_staff, login_url='/forbidden_page/')
def admin_dashboard(request):
    if not (request.user.is_superuser  or request.user.is_staff):
        return redirect('home') 
    
     
    total_bikes = Bike.objects.count()
    total_cars = Car.objects.count()
    total_large_vehicles = LargeVehicle.objects.count()
    total_bookings = Booking.objects.count()
    total_users = get_user_model().objects.filter(is_superuser=False).count()
    unseen_booking_count = Booking.objects.filter(is_seen_by_admin=False).count()

    # Booking status counts
    confirmed_bookings = Booking.objects.filter(status='confirmed').count()
    canceled_bookings = Booking.objects.filter(status='cancelled').count()
    pending_bookings = Booking.objects.filter(status='pending').count()
    completed_bookings = Booking.objects.filter(is_completed=True).count() 
    context = {
        'total_bikes': total_bikes,
        'total_cars': total_cars,
        'total_large_vehicles': total_large_vehicles,
        'total_bookings': total_bookings,
        'total_users': total_users,
        'confirmed_bookings': confirmed_bookings,
        'canceled_bookings': canceled_bookings,
        'pending_bookings': pending_bookings,
        'completed_bookings': completed_bookings,
        'unseen_booking_count' : unseen_booking_count,
    }
    return render(request, 'dashboard.html', context)

@user_passes_test(lambda u: u.is_superuser or u.is_staff, login_url='/forbidden_page/')
def admin_review(request):
    reviews = Review.objects.all().order_by("-created_at") 
    
    if request.method == 'POST' and request.POST.get('action') == 'delete':
        booking_id = request.POST.get('booking_id')
        if booking_id:
            review_to_delete = get_object_or_404(Review, id=booking_id)
            review_to_delete.delete() 
            messages.success(request, "Review deleted successfully.")
        else:
            messages.error(request, "Invalid request. Review not found.")
        
        return redirect('admin_review') 

    return render(request, 'admin_review.html', {'reviews': reviews})

@user_passes_test(lambda u: u.is_superuser or u.is_staff, login_url='/forbidden_page/')
def admin_contact(request):
    contact_messages = Contact.objects.all().order_by('-date', '-date')
    
    # Pagination
    paginator = Paginator(contact_messages, 10)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    if request.method == 'POST' and request.POST.get('action') == 'delete':
        contact_id = request.POST.get('contact_id')
        contact = get_object_or_404(Contact, id=contact_id)
        contact.delete()  
        messages.success(request, "Contact message deleted successfully.")  
        return redirect('admin_contact')  

    return render(request, 'admin_contact.html', {'page_obj': page_obj})

@user_passes_test(lambda u: u.is_superuser or u.is_staff, login_url='/forbidden_page/')
def admin_bike(request):
    bikes = Bike.objects.all().order_by('-id')  
    return render(request, 'bike.html', {'bikes': bikes})

@user_passes_test(lambda u: u.is_superuser or u.is_staff, login_url='/forbidden_page/')
def bike_detail(request, bike_id):
    bike = get_object_or_404(Bike, id=bike_id) 

    return render(request, 'bike_detail.html', {'bike': bike})

@user_passes_test(lambda u: u.is_superuser or u.is_staff, login_url='/forbidden_page/')
def add_bike(request):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        price_per_day = request.POST['price_per_day']
        available = request.POST.get('available', False)
        featured_vehicle = request.POST.get('featured_vehicle', False)
        engine_capacity = request.POST['engine_capacity']
        bike_type = request.POST['bike_type']
        image = request.FILES['image']        
        
        bike=Bike.objects.create(
            name=name,
            description=description,
            price_per_day=price_per_day,
            available=bool(available),
            featured_vehicle=bool(featured_vehicle),
            engine_capacity=engine_capacity,
            bike_type=bike_type,
            image=image
        )
        messages.success(request, f'{bike.name}  successfully!')
        return redirect('bike')

    return render(request, 'add_bike.html')

@user_passes_test(lambda u: u.is_superuser or u.is_staff, login_url='/forbidden_page/')
def edit_bike(request, bike_id):
    bike = get_object_or_404(Bike, id=bike_id)

    if request.method == 'POST' and request.POST.get('action') == 'delete':
        bike.delete()
        messages.success(request, " deleted successfully!")  
        return redirect('bike')
    
    if request.method == 'POST':
        bike.name = request.POST['name']
        bike.description = request.POST['description']
        bike.price_per_day = request.POST['price_per_day']
        bike.available = 'available' in request.POST
        bike.featured_vehicle = 'featured_vehicle' in request.POST
        bike.engine_capacity = request.POST['engine_capacity']
        bike.bike_type = request.POST['bike_type']
        
        if 'image' in request.FILES:
            bike.image = request.FILES['image']
        bike.save()
        
        messages.success(request, f'{bike.name} updated successfully!')
        return redirect('bike')
   
    return render(request, 'bike_details.html', {'bike': bike})

@user_passes_test(lambda u: u.is_superuser or u.is_staff, login_url='/forbidden_page/')
def delete_bike(request, bike_id):
    bike = get_object_or_404(Bike, id=bike_id)
    if request.method == 'POST':
        bike.delete()
        
        messages.success(request,  f'{bike.name} deleted successfully!')
        return redirect('bike')
    
    
@user_passes_test(lambda u: u.is_superuser or u.is_staff, login_url='/forbidden_page/')
def admin_car(request):
    cars=Car.objects.all().order_by('-id')
    return render(request,'car.html', {'cars':cars})

@user_passes_test(lambda u: u.is_superuser or u.is_staff, login_url='/forbidden_page/')
def car_detail(request, car_id):
    car= get_object_or_404(Car, id=car_id) 

    return render(request, 'car_details.html', {'car': car})

@user_passes_test(lambda u: u.is_superuser or u.is_staff, login_url='/forbidden_page/')
def add_car(request):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        price_per_day = request.POST['price_per_day']
        available = request.POST.get('available', False)
        featured_vehicle = request.POST.get('featured_vehicle', False)
        seating_capacity = request.POST['seating_capacity']
        fuel_type = request.POST['fuel_type']
        transmission_type = request.POST['transmission_type']
        needs_driver = request.POST.get('needs_driver', False)
        image = request.FILES['image']  # Handle image file

        car = Car.objects.create(
            name=name,
            description=description,
            price_per_day=price_per_day,
            available=bool(available),
            featured_vehicle=bool(featured_vehicle),
            seating_capacity=seating_capacity,
            fuel_type=fuel_type,
            transmission_type=transmission_type,
            image=image
        )
        messages.success(request, f'{car.name} added successfully!')
        return redirect('car')  

    return render(request, 'add_car.html') 

@user_passes_test(lambda u: u.is_superuser or u.is_staff, login_url='/forbidden_page/')
def edit_car(request, car_id):
    car = get_object_or_404(Car, id=car_id) 

    if request.method == 'POST' and request.POST.get('action') == 'delete':
        car.delete()
        messages.success(request, " deleted successfully!")  
        return redirect('car')

    if request.method == 'POST':
        car.name = request.POST['name']
        car.description = request.POST['description']
        car.price_per_day = request.POST['price_per_day']
        car.available = 'available' in request.POST
        car.featured_vehicle = 'featured_vehicle' in request.POST
        car.seating_capacity = request.POST['seating_capacity']
        car.fuel_type = request.POST['fuel_type']
        car.transmission_type = request.POST['transmission_type']

        if 'image' in request.FILES:
            car.image = request.FILES['image']
        
        car.save()  

        messages.success(request, f'{car.name} updated successfully!')
        return redirect('car')  

    return render(request, 'car_details.html', {'car': car})  

@user_passes_test(lambda u: u.is_superuser or u.is_staff, login_url='/forbidden_page/')
def delete_car(request, car_id):
    car = get_object_or_404(Car, id=car_id) 
    if request.method == 'POST':
        car.delete() 
        
        messages.success(request, f'{car.name} deleted successfully!')
        return redirect('car')
    
@user_passes_test(lambda u: u.is_superuser or u.is_staff, login_url='/forbidden_page/')
def admin_large_vehicle(request):
    large_vehicles = LargeVehicle.objects.all().order_by('-id')
    return render(request, 'large_vehicle.html', {'large_vehicles': large_vehicles})

@user_passes_test(lambda u: u.is_superuser or u.is_staff, login_url='/forbidden_page/')
def large_vehicle_detail(request, large_vehicle_id):
    large_vehicle = get_object_or_404(LargeVehicle, id=large_vehicle_id) 
    return render(request, 'large_vehicle_details.html', {'large_vehicle': large_vehicle})

@user_passes_test(lambda u: u.is_superuser or u.is_staff, login_url='/forbidden_page/')
def add_large_vehicle(request):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        price_per_day = request.POST['price_per_day']
        available = request.POST.get('available', False)
        featured_vehicle = request.POST.get('featured_vehicle', False)
        seating_capacity = request.POST['seating_capacity']
        image = request.FILES['image']  # Handle image file

        large_vehicle = LargeVehicle.objects.create(
            name=name,
            description=description,
            price_per_day=price_per_day,
            available=bool(available),
            featured_vehicle=bool(featured_vehicle),
            seating_capacity=seating_capacity,
            
            image=image
        )
        messages.success(request, f'{large_vehicle.name} added successfully!')
        return redirect('large_vehicle')  # Redirect to large vehicle list

    return render(request, 'add_large_vehicle.html')

@user_passes_test(lambda u: u.is_superuser or u.is_staff, login_url='/forbidden_page/')
def edit_large_vehicle(request, large_vehicle_id):
    large_vehicle = get_object_or_404(LargeVehicle, id=large_vehicle_id) 

    if request.method == 'POST' and request.POST.get('action') == 'delete':
        large_vehicle.delete()
        messages.success(request, " deleted successfully!")  
        return redirect('large_vehicle')

    if request.method == 'POST':
        large_vehicle.name = request.POST['name']
        large_vehicle.description = request.POST['description']
        large_vehicle.price_per_day = request.POST['price_per_day']
        large_vehicle.available = 'available' in request.POST
        large_vehicle.featured_vehicle = 'featured_vehicle' in request.POST
        large_vehicle.seating_capacity = request.POST['seating_capacity']
        large_vehicle.needs_driver = 'needs_driver' in request.POST

        if 'image' in request.FILES:
            large_vehicle.image = request.FILES['image']
        
        large_vehicle.save()

        messages.success(request, f'{large_vehicle.name} updated successfully!')
        return redirect('large_vehicle')

    return render(request, 'large_vehicle_details.html', {'large_vehicle': large_vehicle})

@user_passes_test(lambda u: u.is_superuser or u.is_staff, login_url='/forbidden_page/')
def delete_large_vehicle(request, large_vehicle_id):
    large_vehicle = get_object_or_404(LargeVehicle, id=large_vehicle_id)
    if request.method == 'POST':
        large_vehicle.delete()

        messages.success(request, f'{large_vehicle.name} deleted successfully!')
        return redirect('large_vehicle')
    

@user_passes_test(lambda u: u.is_superuser or u.is_staff, login_url='/forbidden_page/')
@staff_member_required
def admin_booking(request):
    bookings= Booking.objects.all().order_by('-created')
    paginator = Paginator(bookings, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    bookings.filter(is_seen_by_admin=False).update(is_seen_by_admin=True)
    return render(request, 'admin_booking.html', {
        'page_obj': page_obj,
        'bookings': bookings,
    })
@user_passes_test(lambda u: u.is_superuser or u.is_staff, login_url='/forbidden_page/')
def booking_detail(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if not booking.is_seen_by_admin:
        booking.is_seen_by_admin = True
        booking.save()  
    return render(request, 'booking_details.html', {'booking': booking})

@user_passes_test(lambda u: u.is_superuser or u.is_staff, login_url='/forbidden_page/')
def add_booking(request):
    if request.method == 'POST':
        user_email = request.POST['user']       
        vehicle = request.POST['vehicle']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        status = request.POST['status']
        payment_status = 'Paid' if 'payment_status' in request.POST else 'Unpaid'
        user = get_object_or_404(get_user_model(), email=user_email)
        
        
        # Create the booking object
        booking = Booking.objects.create(
            user=user,
            vehicle=vehicle,
            start_date=start_date,
            end_date=end_date,
            status=status,
            payment_status=payment_status
        )
        messages.success(request, f'Booking for {booking.user} added successfully!')
        return redirect('admin_booking')  # Redirect to bookings list
    
    # You can add any forms or context you need here
    return render(request, 'add_booking.html')

@user_passes_test(lambda u: u.is_superuser or u.is_staff, login_url='/forbidden_page/')
def edit_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if request.method == 'POST' and request.POST.get('action') == 'delete':
        booking.delete()
        messages.success(request, "Booking deleted successfully!")  
        return redirect('admin_booking')
    
    if request.method == 'POST':
        try:
            booking.user = User.objects.get(email=request.POST['user'])
            booking.phone_number = request.POST['phone_number']
            booking.start_date = request.POST['start_date']
            booking.end_date = request.POST['end_date']
            booking.vehicle_type = request.POST['vehicle_type']
            booking.vehicle = request.POST['vehicle']
            booking.total_days = int(request.POST['total_days'])
            booking.total_amount = float(request.POST['total_amount'])
            booking.status = request.POST['status']
            booking.self_drive = 'self_drive' in request.POST
            booking.license_document = request.FILES.get('license_document')
            booking.drop_off_required = 'drop_off_required' in request.POST
            booking.drop_off_address = request.POST['drop_off_address']
            booking.special_requirements = request.POST['special_requirements']
            booking.is_completed = 'is_completed' in request.POST
            booking.payment_status = request.POST.get('payment_status', 'Unpaid')        # Save the changes
        
            booking.save()
            messages.success(request, "Booking updated successfully!")
        except ValidationError as e:
            messages.error(request, str(e))
        
        return redirect('admin_booking')
    return render(request, 'booking_details.html', {'booking': booking})

@user_passes_test(lambda u: u.is_superuser or u.is_staff, login_url='/forbidden_page/')
def delete_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if request.method == 'POST':
        booking.delete()
        
        messages.success(request, f'Booking for {booking.user} deleted successfully!')
        return redirect('admin_booking')
    return redirect('admin_booking')

@user_passes_test(lambda u: u.is_superuser or u.is_staff, login_url='/forbidden_page/')
def admin_user_list(request):
    users = CustomUser.objects.filter().order_by('-date_joined')  
    
    paginator = Paginator(users, 10)  # Paginate with 10 users per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'user_list.html', {'page_obj': page_obj})

@user_passes_test(lambda u: u.is_superuser or u.is_staff, login_url='/forbidden_page/')
@staff_member_required
def admin_user_detail(request, user_id):
    user = get_object_or_404(get_user_model(), id=user_id)
    return render(request, 'user_detail.html', {'user': user})

@user_passes_test(lambda u: u.is_superuser or u.is_staff, login_url='/forbidden_page/')
@staff_member_required
def add_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        phone=request.POST.get('phone')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirmpassword=request.POST['confirmpassword']
        is_active = request.POST.get('is_active') == 'on'
        is_staff = request.POST.get('is_staff') == 'on'
        is_superuser = request.POST.get('is_superuser') == 'on'

        if is_superuser:
            is_staff = True
            
        name_regex = r'^[A-Za-z ]{2,50}$'
        if not re.match(name_regex, username):
            messages.error(request, "Name can only contain letters ")
            return render(request, 'add_user.html', {'name': username, 'email': email, 'phone': phone})
        
        if CustomUser.objects.filter(email=email).first():
            messages.error(request, "Email already taken.")
            return render(request, 'add_user.html', {'name': username, 'email': email, 'phone': phone})
        
        if CustomUser.objects.filter(phone=phone).exists():
            messages.error(request, "Phone number is already taken.")
            return render(request, 'add_user.html', {'name': username, 'email': email, 'phone': phone})
         
        
        phone_regex = r'^9\d{9}$'
        if not re.match(phone_regex, phone):
            messages.error(request, "Enter a 10-digit  number starting with 9.")
            return render(request, 'add_user.html', {'name': username, 'email': email, 'phone': phone})
        
        # Password Validation
        PASSWORD_REGEX = r'^.{8,}$'
        if not re.match(PASSWORD_REGEX, password):
            messages.error(request, "Password must be at least 8 characters long")
            return render(request, 'add_user.html', {'name': username, 'email': email, 'phone': phone})

        elif password != confirmpassword:
            messages.error(request, "Password and confirm password do not match.")
            return render(request, 'register.html', {'name': username, 'email': email, 'phone': phone})
        
        
        
        if not email or not username or not password:
            messages.error(request, "Email, Username, and Password are required.")
            return redirect('add_user')

        User = get_user_model()
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "A user with this email already exists.")
            return redirect('add_user')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "A user with this username already exists.")
            return redirect('add_user')

        # Create the user
        user = User.objects.create_user(
            email=email,
            phone=phone,
            username=username,
            password=password
        )
        user.is_active=is_active
        user.is_staff=is_staff
        user.is_superuser=is_superuser
        user.date_joined=timezone.now()
        user.last_login=timezone.now()
        
        user.save()
        messages.success(request, f' {user.username} added successfully!')
        return redirect('user')
    
    current_time = timezone.now()

    return render(request, 'add_user.html', {
        'current_time': current_time
    })

@user_passes_test(lambda u: u.is_superuser or u.is_staff, login_url='/forbidden_page/')
@staff_member_required
def edit_user(request, user_id):
    user = get_object_or_404(get_user_model(), id=user_id)

    if request.method == 'POST'and request.POST.get('action') == 'delete':
        user.delete()
        messages.success(request, f'{user.username} deleted successfully!')
        return redirect('user')

    if request.method == 'POST':
        user.email = request.POST.get('email', user.email)
        user.username = request.POST.get('username', user.username)
        user.first_name = request.POST.get('first_name', user.username)
        
        if 'password' in request.POST:
            user.set_password(request.POST['password'])  
        
        user.is_active = request.POST.get('is_active') == 'on'
        user.is_staff = request.POST.get('is_staff') == 'on'
        user.is_superuser = request.POST.get('is_superuser') == 'on'
        
        
        if user.is_superuser:
            user.is_staff = True
            
        user.save()
        
        messages.success(request, f'{user.username} updated successfully!')
        return redirect('user')

    return render(request, 'user_detail.html', {'user': user})

@user_passes_test(lambda u: u.is_superuser or u.is_staff, login_url='/forbidden_page/')
@staff_member_required
def delete_user(request, user_id):
    user = get_object_or_404(get_user_model(), id=user_id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, f'{user.username} deleted successfully!')
        return redirect('user')
    
@user_passes_test(lambda u: u.is_superuser or u.is_staff, login_url='/forbidden_page/')
@staff_member_required
def admin_bill(request):
    bills = Bill.objects.all().order_by('-confirmation_time')
   
    paginator = Paginator(bills, 10)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    
    return render(request, 'admin_bill.html', {'page_obj': page_obj})

@user_passes_test(lambda u: u.is_superuser or u.is_staff, login_url='/forbidden_page/')
@staff_member_required
def bill_detail(request, bill_id):
    bill = get_object_or_404(Bill, id=bill_id)
    return render(request, 'bill_detail.html', {'bill': bill})

@user_passes_test(lambda u: u.is_superuser or u.is_staff, login_url='/forbidden_page/')
@staff_member_required
def add_bill(request):
    if request.method == 'POST':
        booking_id = request.POST.get('booking_id')
        payment_status = request.POST.get('payment_status')

        booking = get_object_or_404(Booking, id=booking_id)  
        user = booking.user  

        total_amount = booking.total_amount  

        if Bill.objects.filter(booking=booking).exists():
            messages.error(request, f'A bill for booking ID {booking_id} already exists!')
            return redirect('add_bill')  

        # Create a new bill
        bill = Bill.objects.create(
            booking=booking, 
            user=user,  
            total_amount=total_amount,
            payment_status=payment_status,
        )
        messages.success(request, f'Bill for {user.username} added successfully!')
        return redirect('admin_bill')

    available_booking_ids = Booking.objects.exclude(id__in=Bill.objects.values('booking_id'))
    
    return render(request, 'add_bill.html', {'available_booking_ids': available_booking_ids})

@user_passes_test(lambda u: u.is_superuser or u.is_staff, login_url='/forbidden_page/')
@staff_member_required
def edit_bill(request, bill_id):
    bill = get_object_or_404(Bill, id=bill_id)

    if request.method == 'POST':
        
        if request.POST.get('action') == 'delete':
           
            bill.delete()
            messages.success(request, 'Bill deleted successfully.')
            return redirect('admin_bill')  

        bill.total_amount = request.POST.get('total_amount')
        bill.payment_status = request.POST.get('payment_status')

       
        bill.save()
        messages.success(request, f'Bill for {bill.user.username} updated successfully!')

        return redirect('admin_bill')  

    return render(request, 'bill_detail.html', {'bill': bill})

@user_passes_test(lambda u: u.is_superuser or u.is_staff, login_url='/forbidden_page/')
@staff_member_required
def delete_bill(request, bill_id):
    bill = get_object_or_404(Bill, id=bill_id)
    if request.method == 'POST':
        bill.delete()
        messages.success(request, f'Bill for {bill.user.username} deleted successfully!')
        return redirect('admin_bill')
    

from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
import random


def admin_reset_pass(request):
    if request.method == "POST":
        email = request.POST.get("email")

        user = CustomUser.objects.filter(email=email, is_superuser=True)or CustomUser.objects.filter(email=email, is_staff=True).first()

        if not user:
            messages.error(request, "Invalid  email.")
            return redirect( 'admin_reset_pass')

        otp = f"{random.randint(100000, 999999)}"  
        print(f"Generated Admin OTP: {otp}")  

        request.session["admin_reset_email"] = email
        request.session["admin_reset_otp"] = otp

        send_mail(
            "Admin Password Reset OTP",
            f"Your OTP for admin password reset is: {otp}",
            "admin@yourdomain.com",
            [email],
            fail_silently=False,
        )

        return redirect("admin_verify_otp")

    return render(request, 'admin_reset_pass.html')


# Admin OTP Verification

def admin_verify_otp(request):
    otp_verified = False

    if request.method == "POST":
        entered_otp = request.POST.get("otp")
        stored_otp = request.session.get("admin_reset_otp")

        if stored_otp and str(stored_otp) == entered_otp:
            otp_verified = True
            return render(request, "admin_verify_otp.html", {"otp_verified": True})
        else:
            messages.error(request, "Invalid OTP. Please try again.")
            return redirect("admin_verify_otp")

    return render(request, "admin_verify_otp.html", {"otp_verified": otp_verified})


# Admin Password Save

def admin_save_password(request):
    if request.method == "POST":
        email = request.session.get("admin_reset_email")
        user = CustomUser.objects.filter(email=email, is_superuser=True).first()

        if not user:
            messages.error(request, "Invalid request. Please try again.")
            return redirect("admin_verify_otp")

        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        # Password validation
        PASSWORD_REGEX = r'^.{8,}$'  # Password must be at least 8 characters long
        if not re.match(PASSWORD_REGEX, new_password):
            messages.error(request, "Password must be at least 8 characters long.")
            return redirect("admin_verify_otp")

        
        if new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("admin_verify_otp")

        user.password = make_password(new_password)
        user.save()

        messages.success(request, "Password successfully reset. Please log in.")
        return redirect("admin_login")

    return redirect("admin_verify_otp")


# Forbidden Page for Non-Admins
def forbidden_page(request):
    return render(request, 'forbidden_page.html')
