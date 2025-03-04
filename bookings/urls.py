from django.urls import path, include
from rest_framework.routers import DefaultRouter

from rest_framework.routers import DefaultRouter
from .views import BookingViewSet
from .views import RevenueReportView, BankFeesReportView
from .auth_views import RegisterView, CustomObtainAuthToken

router = DefaultRouter()
router.register(r'bookings', BookingViewSet)

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='api_register'),
    path('auth/login/', CustomObtainAuthToken.as_view(), name='api_token_auth'),
    path('', include(router.urls)),
    path('reports/revenue/', RevenueReportView.as_view(), name='revenue-report'),
    path('reports/bank-fees/', BankFeesReportView.as_view(), name='bank-fees-report'),
]
