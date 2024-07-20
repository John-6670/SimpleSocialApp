from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from .models import Post, Comment, Like


class CommentListCreateSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    likes_count = serializers.SerializerMethodField()
    liked_by_user = serializers.SerializerMethodField()
    parent = serializers.PrimaryKeyRelatedField(queryset=Comment.objects.all(), required=False)

    class Meta:
        model = Comment
        fields = ['id', 'author', 'post', 'content', 'likes_count', 'liked_by_user', 'parent']
        read_only_fields = ['id', 'author', 'post', 'likes_count', 'liked_by_user', 'parent']
        search_fields = ['content', 'author__username']

    def create(self, validated_data):
        return Comment.objects.create(**validated_data)

    def get_likes_count(self, obj):
        return Like.objects.filter(content_type=ContentType.objects.get_for_model(Comment), object_id=obj.id).count()

    def get_liked_by_user(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return False

        return Like.objects.filter(user=user, content_type=ContentType.objects.get_for_model(Comment),
                                   object_id=obj.id).exists()


class CommentRetrieveUpdateDestroySerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    likes_count = serializers.SerializerMethodField()
    liked_by_user = serializers.SerializerMethodField()
    parent = serializers.PrimaryKeyRelatedField(queryset=Comment.objects.all(), required=False)

    class Meta:
        model = Comment
        fields = ['id', 'author', 'post', 'content', 'likes_count', 'liked_by_user', 'parent']
        read_only_fields = ['id', 'author', 'post', 'likes_count', 'liked_by_user']

    def get_likes_count(self, obj):
        return Like.objects.filter(content_type=ContentType.objects.get_for_model(Comment), object_id=obj.id).count()

    def get_liked_by_user(self, obj):
        user = self.context.get('request').user
        if not user.is_authenticated:
            return False

        return Like.objects.filter(user=user, content_type=ContentType.objects.get_for_model(Comment),
                                   object_id=obj.id).exists()


class PostUpdateSerializer(serializers.ModelSerializer):
    comments = CommentListCreateSerializer(many=True, read_only=True)
    author = serializers.ReadOnlyField(source='author.username')
    likes_count = serializers.SerializerMethodField()
    liked_by_user = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'author', 'content', 'post_img', 'created_at', 'updated_at', 'likes_count', 'liked_by_user', 'comments_count',
                  'comments']
        read_only_fields = ['id', 'author', 'created_at', 'updated_at', 'likes_count', 'liked_by_user', 'comments_count',
                            'comments']

    def get_likes_count(self, obj):
        return Like.objects.filter(content_type=ContentType.objects.get_for_model(Post), object_id=obj.id).count()

    def get_liked_by_user(self, obj):
        user = self.context.get('request').user
        if not user.is_authenticated:
            return False

        return Like.objects.filter(user=user, content_type=ContentType.objects.get_for_model(Post),
                                   object_id=obj.id).exists()

    def get_comments_count(self, obj):
        return Comment.objects.filter(post=obj).count()


class PostListCreateSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    likes_count = serializers.SerializerMethodField()
    liked_by_user = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'author', 'content', 'post_img', 'created_at', 'updated_at', 'likes_count', 'liked_by_user',
                  'comments_count']
        read_only_fields = ['id', 'author', 'created_at', 'updated_at', 'likes_count', 'liked_by_user',
                            'comments_count']
        search_fields = ['content', 'author__username']

    def create(self, validated_data):
        return Post.objects.create(**validated_data)

    def get_likes_count(self, obj):
        return Like.objects.filter(content_type=ContentType.objects.get_for_model(Post), object_id=obj.id).count()

    def get_liked_by_user(self, obj):
        user = self.context.get('request').user
        if not user.is_authenticated:
            return False

        return Like.objects.filter(user=user, content_type=ContentType.objects.get_for_model(Post),
                                   object_id=obj.id).exists()

    def get_comments_count(self, obj):
        return Comment.objects.filter(post=obj).count()


class LikeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Like
        fields = ['id', 'user', 'content_type', 'object_id', 'created_at']
        read_only_fields = ['id', 'user', 'content_type', 'object_id', 'created_at']
