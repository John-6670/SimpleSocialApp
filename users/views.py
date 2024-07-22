from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.forms import model_to_dict
from django.http import JsonResponse, Http404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status, permissions, filters
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response

from users.models import Follow
from users.serializers import UserLoginSerializer, LogoutSerializer, UserRegistrationSerializer, \
    UserInformationSerializer, PasswordChangeSerializer, FollowSerializer, UserSmallInformationSerializer


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
            profile = user.profile
            profile_dic = model_to_dict(profile)
            # del profile_dic['user']
            profile_dic['profile_pic'] = request.build_absolute_uri(profile_dic['profile_pic'].url)
            response = JsonResponse({'message': 'Login successful', 'user': profile_dic})
            response.status_code = status.HTTP_200_OK
            return response

        return Response({'message': 'username or password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(generics.GenericAPIView):
    serializer_class = LogoutSerializer

    def post(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response({'message': 'You are not logged in'}, status=status.HTTP_401_UNAUTHORIZED)

        logout(request)
        response = JsonResponse({'message': 'Logout successful', 'redirect_url': '/users/login'})
        response.status_code = status.HTTP_204_NO_CONTENT
        return response


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


class UserCreate(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        login(request, user)
        user_dic = model_to_dict(user)
        del user_dic['password']
        response = JsonResponse({'message': 'User created', 'user': user_dic})
        response.status_code = status.HTTP_201_CREATED
        return response


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
