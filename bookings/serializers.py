from rest_framework import serializers
from .models import Booking, RentedItem

class RentedItemSerializer(serializers.ModelSerializer):
    unit = serializers.IntegerField(default=1)

    class Meta:
        model = RentedItem
        fields = ['id', 'name', 'price', 'unit']

    def to_representation(self, instance):
        # Get the default representation
        ret = super().to_representation(instance)
        # Try to convert 'unit' to an integer; if it fails, default to 1.
        try:
            # If ret['unit'] is an empty string or any value that can't be cast to int,
            # int() will raise a ValueError, and we will catch that.
            ret['unit'] = int(ret['unit'])
        except (ValueError, TypeError):
            ret['unit'] = 1
        return ret

class BookingSerializer(serializers.ModelSerializer):
    # For GET requests, include nested rented items by mapping the reverse relation.
    rented_items = RentedItemSerializer(many=True, read_only=True, source='renteditem_set')
    # For POST/PUT, use a write-only field to accept nested data.
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
        rented_items_data = validated_data.pop('rented_items_data', [])
        booking = Booking.objects.create(**validated_data)
        for item_data in rented_items_data:
            RentedItem.objects.create(booking=booking, **item_data)
        return booking

    def update(self, instance, validated_data):
        rented_items_data = validated_data.pop('rented_items_data', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if rented_items_data is not None:
            instance.renteditem_set.all().delete()
            for item_data in rented_items_data:
                RentedItem.objects.create(booking=instance, **item_data)
        return instance
