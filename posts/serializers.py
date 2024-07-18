from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from .models import Post, Comment, Like


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class PostUpdateSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    author = serializers.ReadOnlyField(source='author.username')
    likes_count = serializers.SerializerMethodField()
    liked_by_user = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'author', 'content', 'created_at', 'updated_at', 'likes_count', 'liked_by_user', 'comments']
        read_only_fields = ['id', 'author', 'created_at', 'updated_at', 'likes_count', 'liked_by_user', 'comments']

    def get_likes_count(self, obj):
        return Like.objects.filter(content_type=ContentType.objects.get_for_model(Post), object_id=obj.id).count()

    def get_liked_by_user(self, obj):
        user = self.context.get('request').user
        return Like.objects.filter(user=user, content_type=ContentType.objects.get_for_model(Post),
                                   object_id=obj.id).exists()


class PostListCreateSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'author', 'content', 'created_at', 'updated_at', 'likes_count']
        read_only_fields = ['id', 'author', 'created_at', 'updated_at', 'likes_count']

    def create(self, validated_data):
        return Post.objects.create(**validated_data)

    def get_likes_count(self, obj):
        return Like.objects.filter(content_type=ContentType.objects.get_for_model(Post), object_id=obj.id).count()


class LikeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Like
        fields = ['id', 'user', 'content_type', 'object_id', 'created_at']
        read_only_fields = ['id', 'user', 'content_type', 'object_id', 'created_at']
