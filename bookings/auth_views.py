from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

User = get_user_model()

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        if not email or not password:
            return Response(
                {"error": "Please provide both email and password"},
                status=status.HTTP_400_BAD_REQUEST
            )
        if User.objects.filter(email=email).exists():
            return Response(
                {"error": "Email already exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        user = User(email=email, username=email, password=make_password(password))
        user.is_staff = True  # Mark as admin if needed
        user.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=status.HTTP_201_CREATED)

class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")
        if not email or not password:
            return Response(
                {"error": "Please provide email and password"},
                status=status.HTTP_400_BAD_REQUEST
            )
        user = authenticate(username=email, password=password)
        if not user:
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_400_BAD_REQUEST
            )
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key})
