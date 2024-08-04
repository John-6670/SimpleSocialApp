import os

import jwt
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from dotenv import load_dotenv
from rest_framework import generics, status, permissions, filters
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse

from users.models import Follow
from users.serializers import *
from utils.utils import EmailHelper


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

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = serializer.data
        user_email = User.objects.get(username=user['username'])
        EmailHelper.send_email(user_email)

        return Response({'Message': 'User created'}, status=status.HTTP_201_CREATED)


class VerifyEmail(generics.RetrieveAPIView):
    serializer_class = EmailVerificationSerializer

    def get(self, request, *args, **kwargs):
        token = request.GET.get('token')
        try:
            load_dotenv()
            payload = jwt.decode(token, os.environ.get('SECRET_KEY'), algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])
            profile = Profile.objects.get(user=user)
            if not profile.is_verified:
                profile.is_verified = True
                profile.save()

            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


class PasswordChangeView(generics.UpdateAPIView):
    serializer_class = PasswordChangeSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)


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
