from rest_framework import serializers
from .models import Booking, RentedItem

class RentedItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = RentedItem
        fields = ['id', 'name', 'price', 'unit']

class BookingSerializer(serializers.ModelSerializer):
    rented_items = RentedItemSerializer(many=True, write_only=True)
    total_fee = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Booking
        fields = [
            'id', 'client_name', 'address', 'payment_method',
            'delivery_date', 'current_date', 'expected_return_date',
            'transport_cost', 'discount', 'payment_status',
            'rented_items', 'total_fee'
        ]

    def get_total_fee(self, obj):
        return obj.total_fee

    def create(self, validated_data):
        rented_items_data = validated_data.pop('rented_items')
        booking = Booking.objects.create(**validated_data)
        for item_data in rented_items_data:
            RentedItem.objects.create(booking=booking, **item_data)
        return booking

    def update(self, instance, validated_data):
        rented_items_data = validated_data.pop('rented_items', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if rented_items_data is not None:
            instance.renteditem_set.all().delete()
            for item_data in rented_items_data:
                RentedItem.objects.create(booking=instance, **item_data)
        return instance
