from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.response import Response

from .models import Comment, Post
from .serializers import PostSerializer, CommentSerializer


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


class PostCommentListCreate(generics.ListCreateAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs['id']
        return Comment.objects.filter(post_id=post_id)

    def create(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionDenied("You need to be logged in to comment.")

        post_id = self.kwargs['id']
        post = generics.get_object_or_404(Post, id=post_id)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def test(request):
    return render(request, 'base.html')
