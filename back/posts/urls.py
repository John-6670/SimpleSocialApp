from django.urls import path
from .views import *

urlpatterns = [
    path('', PostListCreate.as_view(), name='list-notes'),
    path('<int:id>/', PostRetrieveUpdateDestroy.as_view(), name='RUD-note'),
    path('<int:id>/comments/', PostCommentListCreate.as_view(), name='list-comments'),
    path('test/', test, name='test'),
]