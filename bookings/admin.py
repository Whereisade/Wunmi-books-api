from django.contrib import admin
from .models import Booking, RentedItem

class RentedItemInline(admin.TabularInline):
    model = RentedItem
    extra = 1  # How many blank items to display by default

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'delivery_date', 'payment_method', 'total_fee')
    search_fields = ('client_name', 'address')
    list_filter = ('payment_method', 'payment_status', 'delivery_date')
    inlines = [RentedItemInline]
