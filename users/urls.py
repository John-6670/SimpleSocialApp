from django.urls import path

from .views import *

urlpatterns = [
    path('', UserListView.as_view(), name='users'),

    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', UserCreate.as_view(), name='register'),

    path('profile/', ShowUserView.as_view(), name='profile'),
    path('profile/followers/', UserFollowersListView.as_view(), name='profile_followers'),
    path('profile/followings/', UserFollowingsListView.as_view(), name='profile_following'),

    path('password-change/', PasswordChangeView.as_view(), name='password-change'),

    path('<str:username>/', UserRetrieveView.as_view(), name='user'),
    path('<str:username>/follow/', FollowUserView.as_view(), name='follow'),
    path('<str:username>/followers/', UserFollowersListView.as_view(), name='followers'),
    path('<str:username>/followings/', UserFollowingsListView.as_view(), name='following'),
]
