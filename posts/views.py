from rest_framework import generics, status
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.response import Response

from .models import Comment, Post
from .serializers import PostListCreateSerializer, PostUpdateSerializer, CommentSerializer


# Create your views here.
class PostListCreate(generics.ListCreateAPIView):
    serializer_class = PostListCreateSerializer
    queryset = Post.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        if not user.is_authenticated:
            raise PermissionDenied('You must be logged in.')

        serializer.save(author=user)


class PostRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostUpdateSerializer
    lookup_field = 'id'

    def get_object(self):
        return Post.objects.get(id=self.kwargs['id'])

    def update(self, request, *args, **kwargs):
        post = self.get_object()
        user = self.request.user

        if not user.is_authenticated:
            raise PermissionDenied('You must log in first.')

        if post.author.username != user.username:
            raise PermissionDenied('You do not have permission to edit this post.')

        return super().update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        post = self.get_object()
        user = self.request.user

        if not user.is_authenticated:
            raise PermissionDenied('You must log in first.')

        if post.author.username != user.username:
            raise PermissionDenied('You do not have permission to delete this post.')

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


class PostCommentRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    lookup_field = 'id'
    queryset = Comment.objects.all()

    def update(self, request, *args, **kwargs):
        comment_id = self.kwargs['id']
        comment = generics.get_object_or_404(Comment, id=comment_id)
        user = self.request.user
        if comment.author != request.user or not user.is_superuser:
            raise PermissionDenied("You do not have permission to edit this post.")

        return super().update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        comment_id = self.kwargs['id']
        comment = generics.get_object_or_404(Comment, id=comment_id)
        user = self.request.user
        if comment.author is not request.user or not user.is_superuser:
            raise PermissionDenied("You do not have permission to delete this post.")

        return super().delete(request, *args, **kwargs)
