from django import template
# from InfiniteRide.models import Invoice  
register = template.Library()

# @register.filter
# def get_invoice_by_booking(bookings, booking_id):
#     """Custom filter to get the invoice for a particular booking."""
#     return Invoice.objects.filter(booking__id=booking_id).first()
