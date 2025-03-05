from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Booking
from .serializers import BookingSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from collections import defaultdict
from decimal import Decimal

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]


class RevenueReportView(APIView):
    """
    Endpoint: GET /api/reports/revenue/?month=...&year=...
    Returns total revenue (sum of booking.total_fee) filtered by optional month/year.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        month = request.query_params.get('month')  # e.g., "3" for March
        year = request.query_params.get('year')    # e.g., "2025"

        # Start with all bookings
        queryset = Booking.objects.all()

        # Filter by year/month if provided
        if year:
            queryset = queryset.filter(delivery_date__year=year)
        if month:
            queryset = queryset.filter(delivery_date__month=month)

        # Sum up the total_fee property in Python
        total_revenue = sum(booking.total_fee for booking in queryset)

        return Response({"total_revenue": total_revenue})

class BankFeesReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        fees_by_bank = defaultdict(lambda: Decimal('0'))
        queryset = Booking.objects.all()

        for booking in queryset:
            fees_by_bank[booking.payment_method] += booking.total_fee

        # Convert the Decimal values to float (or string) for JSON serialization if needed
        result = [
            {"bank": bank, "total_fee": float(total_fee)}
            for bank, total_fee in fees_by_bank.items()
        ]
        return Response({"fees_by_bank": result})