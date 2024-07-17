from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from rest_framework import generics, status, permissions
from rest_framework.response import Response

from users.serializers import LoginSerializer, LogoutSerializer, UserSerializer


# Create your views here.
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

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
        response = JsonResponse({'message': 'Logout successful', 'redirect_url': '/login'})
        response.status_code = status.HTTP_200_OK
        return response


class ShowUserView(generics.RetrieveDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserCreate(generics.CreateAPIView):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        login(request, user)
        response = JsonResponse({'message': 'User created', 'redirect_url': '/posts'})
        response.status_code = status.HTTP_200_OK
        return response
