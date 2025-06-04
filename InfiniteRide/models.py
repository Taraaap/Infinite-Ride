from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.contrib.auth.models import User
import datetime
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

# Create your models here.

class Contact(models.Model):
    name=models.CharField(max_length=122)
    email=models.CharField(max_length=122)
    phone=models.CharField(max_length=15)
    message=models.TextField()
    date=models.DateField()
    
    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=150, blank=True, null=True)  
    email = models.EmailField(unique=True)
    
    username = models.CharField(max_length=150, blank=True, null=True, unique=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [ 'username', 'phone']
    
    def __str__(self):
        return self.email
    
class Vehicle(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='vehicles/', blank=False, null=False)
    available = models.BooleanField(default=True)
    featured_vehicle = models.BooleanField(default=False)
    available = models.BooleanField(default=True)
    class Meta:
        abstract = True
    
    def __str__(self):
        return self.name
    
class Car(Vehicle):
    seating_capacity = models.IntegerField()
    fuel_type = models.CharField(max_length=50)
    transmission_type = models.CharField(max_length=50)
    needs_driver = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Car - {self.name}"
    
class Bike(Vehicle):
    engine_capacity = models.FloatField()
    bike_type = models.CharField(max_length=50)  
    def __str__(self):
        return f"Bike - {self.name}"
    
    
class LargeVehicle(Vehicle):
    seating_capacity = models.IntegerField()
    needs_driver = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name} ({self.seating_capacity} seats)"

User = get_user_model()
class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    car = models.ForeignKey('Car', on_delete=models.SET_NULL, null=True, blank=True)
    bike = models.ForeignKey('Bike', on_delete=models.SET_NULL, null=True, blank=True)
    large_vehicle = models.ForeignKey('LargeVehicle', on_delete=models.SET_NULL, null=True, blank=True)
    total_days = models.PositiveIntegerField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    self_drive = models.BooleanField(default=False)  
    license_document = models.FileField(upload_to='licenses/', null=True, blank=True)  
    drop_off_required = models.BooleanField(default=False) 
    drop_off_address = models.TextField(null=True, blank=True)  
    special_requirements = models.TextField(null=True, blank=True)  
    created = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)
    is_seen_by_admin = models.BooleanField(default=False)
    booking_date = models.DateTimeField(default=datetime.datetime.now,blank=True)
    
    PAYMENT_CHOICES = [
        ("Unpaid", "Unpaid"),
        ("Paid", "Paid"),
    ]
    payment_status = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default="Unpaid")

    
    
    def get_vehicle(self):
        if self.car:
            return self.car.name 
        elif self.bike:
            return self.bike.name 
        elif self.large_vehicle:
            return self.large_vehicle.name  
        return "No vehicle"
    
    def get_vehicle_type(self):
        if self.car:
            return "Car"
        elif self.bike:
            return "Bike"
        elif self.large_vehicle:
            return "Large Vehicle"
        return "Unknown"



def save(self, *args, **kwargs):
        # Ensure user's phone number is saved
        if self.user and hasattr(self.user, 'phone'):
            self.phone_number = self.user.phone  

        # Calculate total days
        if self.start_date and self.end_date:
            self.total_days = (self.end_date - self.start_date).days + 1  # At least 1 day

        # Determine the selected vehicle
        vehicle = self.car or self.bike or self.large_vehicle
        if vehicle:
            self.total_amount = self.total_days * vehicle.price_per_day

        # Validation before saving
        if self.bike and not self.license_document:
            raise ValidationError("License document is required for bike bookings.")

        if self.car and self.self_drive and not self.license_document:
            raise ValidationError("License document is required for self-drive car bookings.")

        if self.drop_off_required and not self.drop_off_address:
            raise ValidationError("Drop-off address is required when drop-off is selected.")
        
        # if not self.special_requests:
        #     self.special_requests = self.special_requests
        
        super().save(*args, **kwargs)
def __str__(self):
    return f"Booking by {self.user.email} ({self.phone_number})- {self.status}"


    
class Review(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} for Booking {self.booking.id}"
    

class Bill(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(
        max_length=10,
        choices=[('unpaid', 'Unpaid'), ('paid', 'Paid')],
        default='paid'
    )
    trade_mark = models.CharField(max_length=10, default="∞")
    confirmation_date = models.DateField(default=datetime.datetime.now,blank=True)
    confirmation_time = models.DateTimeField(default=datetime.datetime.now,blank=True)

    def __str__(self):
        return f"Bill #{self.id} for {self.user.username} - Payment Status: {self.payment_status}"
    
    
