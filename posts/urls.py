from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostListCreate.as_view(), name='list-notes'),
    path('<int:id>/', views.PostRetrieveUpdateDestroy.as_view(), name='RUD-note'),
]