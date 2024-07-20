from django.contrib.contenttypes.models import ContentType
from django.core.serializers import serialize
from django.db.models import Q
from django.http import Http404
from rest_framework import filters
from rest_framework import generics, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from users.models import Follow
from .models import Comment, Post, Like
from .serializers import (PostListCreateSerializer, PostUpdateSerializer, CommentListCreateSerializer, LikeSerializer,
                          CommentRetrieveUpdateDestroySerializer)


# Create your views here.
class PostListCreate(generics.ListCreateAPIView):
    serializer_class = PostListCreateSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    queryset = Post.objects.all()

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        search_term = self.request.query_params.get('search', None)
        if search_term:
            queryset = queryset.filter(
                Q(content__icontains=search_term) |
                Q(author__username__icontains=search_term)
            )
        elif user.is_authenticated:
            following_ids = Follow.objects.filter(follower=user).values_list('following_id', flat=True)
            if following_ids:
                queryset = queryset.filter(author__id__in=following_ids).order_by('-created_at')

        return queryset

    def perform_create(self, serializer):
        user = self.request.user
        if not user.is_authenticated:
            raise PermissionDenied('You must be logged in.')

        serializer.save(author=user)


class PostRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostUpdateSerializer
    lookup_field = 'id'

    def get_object(self):
        post = Post.objects.filter(id=self.kwargs['id']).first()
        if not post:
            raise Http404
        return post

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
    serializer_class = CommentListCreateSerializer
    queryset = Comment.objects.all()

    def get_queryset(self):
        post = Post.objects.filter(id=self.kwargs['id']).first()
        if not post:
            raise Http404

        queryset = super().get_queryset()
        search_term = self.request.query_params.get('search', None)
        if search_term:
            queryset = queryset.filter(
                Q(content__icontains=search_term) |
                Q(author__username__icontains=search_term)
            )
        return queryset

    def create(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionDenied("You need to be logged in to comment.")

        post_id = self.kwargs['id']
        post = generics.get_object_or_404(Post, id=post_id)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(post=post, author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostCommentRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentRetrieveUpdateDestroySerializer
    lookup_field = 'pk'

    def get_object(self):
        post = Post.objects.filter(id=self.kwargs['id']).first()
        if not post:
            raise Http404
        
        comment_id = self.kwargs['pk']
        comment = Comment.objects.filter(id=comment_id).first()
        if not comment:
            raise Http404
        return comment

    def update(self, request, *args, **kwargs):
        comment_id = self.kwargs['pk']
        comment = self.get_object()
        user = self.request.user
        if not user.is_authenticated:
            raise PermissionDenied('You must log in first.')

        if comment.author.username != user.username:
            raise PermissionDenied('You do not have permission to delete this post.')

        return super().update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        comment_id = self.kwargs['pk']
        comment = generics.get_object_or_404(Comment, id=comment_id)
        user = self.request.user
        if not user.is_authenticated:
            raise PermissionDenied('You must log in first.')

        if comment.author.username != user.username:
            raise PermissionDenied('You do not have permission to delete this post.')

        return super().delete(request, *args, **kwargs)


class LikePostView(generics.CreateAPIView):
    serializer_class = LikeSerializer
    queryset = Like.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        if not user.is_authenticated:
            raise PermissionDenied('You must log in first.')

        post = self.get_object()
        like = Like.objects.filter(user=user, content_type=ContentType.objects.get_for_model(post),
                                   object_id=post.id).first()

        # Check if user already liked the post
        if not like:
            serializer.is_valid(raise_exception=True)
            serializer.save(user=user, content_type=ContentType.objects.get_for_model(Post), object_id=post.id)
        else:
            like.delete()

    def get_object(self):
        # Retrieve the post object based on the ID in the URL
        return Post.objects.get(id=self.kwargs['id'])


class LikeCommentView(generics.CreateAPIView):
    serializer_class = LikeSerializer
    queryset = Like.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        if not user.is_authenticated:
            raise PermissionDenied('You must log in first.')

        post = self.get_object()
        like = Like.objects.filter(user=user, content_type=ContentType.objects.get_for_model(Comment),
                                   object_id=post.id).first()

        if not like:
            serializer.is_valid(raise_exception=True)
            serializer.save(user=user, content_type=ContentType.objects.get_for_model(Comment), object_id=post.id)
        else:
            like.delete()

    def get_object(self):
        return Post.objects.get(id=self.kwargs['pk'])
