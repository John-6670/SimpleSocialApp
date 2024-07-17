from django.urls import path

from .views import *

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', ShowUserView.as_view(), name='home'),
    path('register/', UserCreate.as_view(), name='register'),
]