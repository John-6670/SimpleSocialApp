from django.contrib.contenttypes.models import ContentType
from rest_framework import generics, status, serializers
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.response import Response

from .models import Comment, Post, Like
from .serializers import PostListCreateSerializer, PostUpdateSerializer, CommentSerializer, LikeSerializer


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


class LikePostView(generics.CreateAPIView):
    serializer_class = LikeSerializer
    queryset = Like.objects.all()

    def perform_create(self, serializer):
        # Access the post object from the URL using `self.get_object()`
        post = self.get_object()
        user = self.request.user

        # Check if user already liked the post (optional)
        if not Like.objects.filter(user=user, content_type=ContentType.objects.get_for_model(Post), object_id=post.id).exists():
            # Create a new Like object if not already liked
            serializer.save(user=user, content_type=ContentType.objects.get_for_model(Post), object_id=post.id)
        else:
            raise serializers.ValidationError("You already liked this post.")

    def get_object(self):
        # Retrieve the post object based on the ID in the URL
        pk = self.kwargs.get('pk')
        return Post.objects.get(pk=id)
