from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework import generics, status, permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from users.serializers import UserLoginSerializer, LogoutSerializer, UserRegistrationSerializer, UserInformationSerializer, PasswordChangeSerializer


# Create your views here.
class LoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )

        if user is not None:
            login(request, user)
            response = JsonResponse({'message': 'Login successful', 'redirect_url': '/posts'})
            response.status_code = status.HTTP_200_OK
            return response

        return Response({'message': 'username or password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(generics.GenericAPIView):
    serializer_class = LogoutSerializer

    def post(self, request):
        logout(request)
        response = JsonResponse({'message': 'Logout successful', 'redirect_url': '/account/login'})
        response.status_code = status.HTTP_200_OK
        return response


class ShowUserView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserInformationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        user = self.request.user
        if user.is_authenticated:
            return user

        raise PermissionDenied('You are not logged in')


class UserCreate(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        login(request, user)
        response = JsonResponse({'message': 'User created', 'redirect_url': '/posts'})
        response.status_code = status.HTTP_200_OK
        return response


class PasswordChangeView(generics.UpdateAPIView):
    serializer_class = PasswordChangeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        if not user.is_authenticated:
            return Response({'message': 'You are not logged in'}, status=status.HTTP_400_BAD_REQUEST)

        old_password = serializer.validated_data['old_password']
        new_password = serializer.validated_data['new_password']
        confirm_password = serializer.validated_data['confirm_password']
        if not user.check_password(old_password):
            return Response({'message': 'Old password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)
        if new_password != confirm_password:
            return Response({'message': "Passwords don't match"}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        login(request, user)
        response = JsonResponse({'message': 'Password changed successfully', 'redirect_url': '/account'})
        response.status_code = status.HTTP_200_OK
        return response
