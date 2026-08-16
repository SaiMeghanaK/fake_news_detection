from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializers import RegisterSerializer, UserSerializer

class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = RegisterSerializer(
            data=request.data
        )
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    "message": "Registration successful.",
                    "user": UserSerializer(user).data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(
            request,
            username=email,
            password=password
        )
        if user is None:
            return Response(
                {"error": "Invalid email or password."},
                status=status.HTTP_401_UNAUTHORIZED
            )
        refresh = RefreshToken.for_user(user)
        return Response({
            "message": "Login successful.",
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": UserSerializer(user).data
        })

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response(
            UserSerializer(request.user).data
        )

def register_page(request):
    if request.user.is_authenticated:
        return redirect("/")
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get(
            "confirm_password"
        )
        role = request.POST.get("role")
        phone = request.POST.get("phone")
        if not email or not password:
            messages.error(
                request,
                "Email and password are required."
            )
            return render(
                request,
                "accounts/register.html"
            )
        if password != confirm_password:
            messages.error(
                request,
                "Passwords do not match."
            )
            return render(
                request,
                "accounts/register.html"
            )
        if role not in ["writer", "reader"]:
            messages.error(
                request,
                "Invalid role."
            )
            return render(
                request,
                "accounts/register.html"
            )
        if User.objects.filter(
            email=email
        ).exists():
            messages.error(
                request,
                "An account with this email already exists."
            )
            return render(
                request,
                "accounts/register.html"
            )
        user = User.objects.create_user(
            email=email,
            password=password,
            role=role,
            phone=phone
        )
        messages.success(
            request,
            "Registration successful. Please login."
        )
        return redirect("/login/")
    return render(
        request,
        "accounts/register.html"
    )

def login_page(request):
    if request.user.is_authenticated:
        return redirect("/")
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(
            request,
            username=email,
            password=password
        )
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect(
                    "/administrator/dashboard/"
                )
            if user.role == "writer":
                return redirect(
                    "/writer/dashboard/"
                )
            return redirect("/")
        messages.error(
            request,
            "Invalid email or password."
        )
    return render(
        request,
        "accounts/login.html"
    )

def logout_page(request):
    logout(request)
    messages.success(
        request,
        "You have been logged out."
    )
    return redirect("/")

def profile_page(request):
    if not request.user.is_authenticated:
        return redirect("/login/")
    return render(
        request,
        "accounts/profile.html"
    )