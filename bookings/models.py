from django.db import models
from decimal import Decimal

class Booking(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('POLARIS', 'Polaris Bank'),
        ('ACCESS', 'Access Bank'),
        ('FIDELITY', 'Fidelity'),
        ('GT', 'GT Bank'),
        ('FIRST', 'First Bank'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('PAID_AND_SUPPLY', 'PAID AND SUPPLY'),
        ('PAID', 'PAID'),
    ]

    client_name = models.CharField(max_length=255)
    address = models.TextField()
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    delivery_date = models.DateField()
    current_date = models.DateField()
    expected_return_date = models.DateField()
    transport_cost = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES)

    def __str__(self):
        return f'{self.client_name} - {self.delivery_date}'

    @property
    def total_fee(self):
        items_total = sum((item.price for item in self.renteditem_set.all()), Decimal('0'))
        return items_total + self.transport_cost - self.discount


class RentedItem(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.IntegerField(default=1)  # Now a number (quantity)

    def __str__(self):
        return f'{self.name} (x{self.unit}) - {self.price}'
