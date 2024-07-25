from django.contrib.auth import login
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import JsonResponse, Http404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status, permissions, filters
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import Follow
from users.serializers import (UserRegistrationSerializer, UserInformationSerializer, PasswordChangeSerializer,
                               FollowSerializer, UserSmallInformationSerializer)


# Create your views here.
class LogoutView(generics.GenericAPIView):
    def post(self, request):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'You have been logged out'}, status=status.HTTP_200_OK)
        except KeyError:
            return Response({'message': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)


class ShowUserView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserInformationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        user = self.request.user
        if user.is_authenticated:
            return user

        raise PermissionDenied('You are not logged in')


class UserListView(generics.ListAPIView):
    serializer_class = UserSmallInformationSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    queryset = User.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        username = self.request.query_params.get('username', None)
        if username:
            return queryset.filter(username__icontains=username)
        else:
            raise ValidationError("Query parameter 'username' is required")


class UserRetrieveView(generics.RetrieveAPIView):
    serializer_class = UserInformationSerializer
    lookup_field = 'username'

    def get_object(self):
        user = User.objects.filter(username__iexact=self.kwargs['username']).first()
        if not user:
            raise Http404
        return user


class UserCreateView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]

    # def create(self, request, *args, **kwargs):
    #     serializer = self.serializer_class(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     user = serializer.save()
    #     login(request, user)
    #     response = JsonResponse({'message': 'User created', 'redirect_url': '/posts'})
    #     response.status_code = status.HTTP_201_CREATED
    #     return response


class PasswordChangeView(generics.UpdateAPIView):
    serializer_class = PasswordChangeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

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

        user.set_password(new_password)
        user.save()
        login(request, user)
        response = JsonResponse({'message': 'Password changed successfully', 'redirect_url': '/account'})
        response.status_code = status.HTTP_200_OK
        return response


class FollowUserView(generics.CreateAPIView):
    serializer_class = FollowSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return Response({'message': 'You are not logged in'}, status=status.HTTP_401_UNAUTHORIZED)

        username = self.kwargs['username']
        user_to_follow = User.objects.filter(username__iexact=username).first()
        if not user_to_follow:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        if request.user.username == user_to_follow.username:
            return Response({'message': 'You cannot follow yourself'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            Follow.objects.create(follower=request.user, following=user_to_follow)
            return Response({'message': 'User followed'}, status=status.HTTP_201_CREATED)
        except IntegrityError:
            Follow.objects.get(follower=request.user, following=user_to_follow).delete()
            return Response({'message': 'User unfollowed'}, status=status.HTTP_204_NO_CONTENT)


class UserFollowersListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSmallInformationSerializer

    def get_queryset(self):
        try:
            username = self.kwargs['username']
            user = User.objects.filter(username__iexact=username).first()
        except KeyError:
            user = self.request.user

        if not user:
            raise Http404

        follower_ids = Follow.objects.filter(following=user).values_list('follower_id', flat=True)
        return User.objects.filter(id__in=follower_ids)


class UserFollowingsListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSmallInformationSerializer

    def get_queryset(self):
        try:
            username = self.kwargs['username']
            user = User.objects.filter(username__iexact=username).first()
        except KeyError:
            user = self.request.user
        if not user:
            raise Http404

        following_id = Follow.objects.filter(follower=user).values_list('following_id', flat=True)
        return User.objects.filter(id__in=following_id)
