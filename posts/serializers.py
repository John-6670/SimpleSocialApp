from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from .models import Post, Comment, Like


class CommentListCreateSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    likes_count = serializers.SerializerMethodField()
    liked_by_user = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'author', 'post', 'content', 'likes_count', 'liked_by_user']
        read_only_fields = ['id', 'author', 'post', 'likes_count', 'liked_by_user']

    def create(self, validated_data):
        return Comment.objects.create(**validated_data)

    def get_likes_count(self, obj):
        return Like.objects.filter(content_type=ContentType.objects.get_for_model(Comment), object_id=obj.id).count()

    def get_liked_by_user(self, obj):
        user = self.context.get('request').user
        return Like.objects.filter(user=user, content_type=ContentType.objects.get_for_model(Comment),
                                   object_id=obj.id).exists()


class CommentRetrieveUpdateDestroySerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    likes_count = serializers.SerializerMethodField()
    liked_by_user = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'author', 'post', 'content', 'likes_count', 'liked_by_user']
        read_only_fields = ['id', 'author', 'post', 'likes_count', 'liked_by_user']

    def get_likes_count(self, obj):
        return Like.objects.filter(content_type=ContentType.objects.get_for_model(Comment), object_id=obj.id).count()

    def get_liked_by_user(self, obj):
        user = self.context.get('request').user
        return Like.objects.filter(user=user, content_type=ContentType.objects.get_for_model(Comment),
                                   object_id=obj.id).exists()


class PostUpdateSerializer(serializers.ModelSerializer):
    comments = CommentListCreateSerializer(many=True, read_only=True)
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
    liked_by_user = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'author', 'content', 'created_at', 'updated_at', 'likes_count', 'liked_by_user']
        read_only_fields = ['id', 'author', 'created_at', 'updated_at', 'likes_count', 'liked_by_user']

    def create(self, validated_data):
        return Post.objects.create(**validated_data)

    def get_likes_count(self, obj):
        return Like.objects.filter(content_type=ContentType.objects.get_for_model(Post), object_id=obj.id).count()

    def get_liked_by_user(self, obj):
        user = self.context.get('request').user
        return Like.objects.filter(user=user, content_type=ContentType.objects.get_for_model(Post),
                                   object_id=obj.id).exists()


class LikeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Like
        fields = ['id', 'user', 'content_type', 'object_id', 'created_at']
        read_only_fields = ['id', 'user', 'content_type', 'object_id', 'created_at']
