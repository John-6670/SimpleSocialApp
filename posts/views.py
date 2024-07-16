from rest_framework import generics
from rest_framework.exceptions import ValidationError, PermissionDenied
from .serializers import PostSerializer


# Create your views here.
class PostListCreate(generics.ListCreateAPIView):
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        user = self.request.user
        if not serializer.is_valid():
            raise ValidationError("Invalid data.")

        serializer.save(author=user)

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            raise PermissionDenied("You need to be logged in to view notes.")

        return user.posts.all()


class PostRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    lookup_field = 'id'

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            raise PermissionDenied("You need to be logged in to view notes.")

        return user.posts.all()

    def update(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != request.user:
            raise PermissionDenied("You do not have permission to edit this note.")

        return super().update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != request.user:
            raise PermissionDenied("You do not have permission to delete this note.")

        return super().delete(request, *args, **kwargs)
