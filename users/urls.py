from django.urls import path

from .views import *

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ShowUserView.as_view(), name='profile'),
    path('register/', UserCreate.as_view(), name='register'),
    path('password-change/', PasswordChangeView.as_view(), name='password-change'),
    path('', UserListView.as_view(), name='users'),
]
