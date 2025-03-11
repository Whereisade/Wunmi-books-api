from django.contrib import admin
from .models import Booking, RentedItem

class RentedItemInline(admin.TabularInline):
    model = RentedItem
    extra = 1
    fields = ('name', 'price', 'unit')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    inlines = [RentedItemInline]
    list_display = ('client_name', 'payment_method', 'delivery_date', 'payment_status')
    search_fields = ('client_name', 'address')
    list_filter = ('payment_method', 'payment_status', 'delivery_date')
