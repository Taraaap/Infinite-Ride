from django.contrib import admin
from InfiniteRide.models import Contact
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin
from .models import Car, Bike, LargeVehicle
from .models import Vehicle
from .models import Booking, Review, Bill
from django.utils.translation import gettext_lazy as _



class VehicleAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_vehicle_type', 'featured_vehicle')
    list_filter = ('featured_vehicle',)

    def get_vehicle_type(self, obj):
        if isinstance(obj, Car):
            return 'Car'
        elif isinstance(obj, Bike):
            return 'Bike'
        elif isinstance(obj, LargeVehicle):
            return 'Large Vehicle'
        return 'Unknown'
    
    get_vehicle_type.short_description = 'Vehicle Type'
 
    
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user','available', 'start_date', 'end_date', 'get_vehicle', 'status')
    search_fields = ('user__email','car__name', 'bike__name', 'large_vehicle__name', 'start_date', 'end_date')
    list_filter = ('payment_status', 'status')
    def get_vehicle(self, obj):
        return obj.car or obj.bike or obj.large_vehicle
    get_vehicle.short_description = 'Vehicle'


# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Contact)
admin.site.register(Car)
admin.site.register(Bike)
admin.site.register(LargeVehicle)
admin.site.register(Booking)



class ReviewAdmin(admin.ModelAdmin):
    list_display = ('booking', 'user', 'review_text', 'created_at')
    search_fields = ('user__username', 'review_text')

admin.site.register(Review, ReviewAdmin)

def mark_as_paid(modeladmin, request, queryset):
    """
    Custom action to mark selected invoices as 'Paid'
    """
    queryset.update(payment_status='paid')

mark_as_paid.short_description = _('Mark selected invoices as Paid')

class BillAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'invoice_date', 'total_amount', 'payment_status', 'confirmation_date']
    actions = [mark_as_paid]

    def invoice_date(self, obj):
        # Ensure that 'booking' exists and has a start_date attribute
        if hasattr(obj, 'booking') and obj.booking:
            return obj.booking.start_date
        return 'N/A'
    invoice_date.short_description = 'Invoice Date'

admin.site.register(Bill, BillAdmin)