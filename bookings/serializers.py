from rest_framework import serializers
from .models import Booking, RentedItem

class RentedItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = RentedItem
        fields = ['id', 'name', 'price', 'unit']

class BookingSerializer(serializers.ModelSerializer):
    # This field is for GET requests: shows the nested rented items.
    rented_items = RentedItemSerializer(many=True, read_only=True)
    # This field is for write operations: use it when creating/updating bookings.
    rented_items_data = RentedItemSerializer(many=True, write_only=True, required=False)
    total_fee = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Booking
        fields = [
            'id', 'client_name', 'address', 'payment_method',
            'delivery_date', 'current_date', 'expected_return_date',
            'transport_cost', 'discount', 'payment_status',
            'rented_items', 'rented_items_data', 'total_fee'
        ]
        read_only_fields = ['total_fee']

    def get_total_fee(self, obj):
        return obj.total_fee

    def create(self, validated_data):
        # Pop the write-only rented_items_data field; default to empty list if not provided.
        rented_items_data = validated_data.pop('rented_items_data', [])
        booking = Booking.objects.create(**validated_data)
        for item_data in rented_items_data:
            RentedItem.objects.create(booking=booking, **item_data)
        return booking

    def update(self, instance, validated_data):
        # Pop the rented_items_data if provided
        rented_items_data = validated_data.pop('rented_items_data', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if rented_items_data is not None:
            # Delete all existing rented items and recreate them.
            instance.renteditem_set.all().delete()
            for item_data in rented_items_data:
                RentedItem.objects.create(booking=instance, **item_data)
        return instance
