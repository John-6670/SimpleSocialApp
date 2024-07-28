from rest_framework import serializers
from django.contrib.auth.models import User

from posts.models import Post
from posts.serializers import PostListCreateSerializer
from .models import Follow, Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['bio', 'birth_date', 'profile_pic']
        read_only_fields = ['user']


class UserRegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)
    profile = ProfileSerializer(required=False)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'password', 'confirm_password', 'profile']
        write_only_fields = ['password', 'confirm_password']

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords don't match."})
        return attrs

    def create(self, validated_data):
        profile_data = validated_data.pop('profile', None)
        del validated_data['confirm_password']
        user = User.objects.create_user(**validated_data)
        if profile_data:
            Profile.objects.create(user=user, **profile_data)
        return user


class UserSmallInformationSerializer(serializers.ModelSerializer):
    followers = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'followers', 'following', 'profile']
        read_only_fields = ['username', 'id', 'followers', 'following', 'profile']

    def get_followers(self, obj):
        return obj.followers.count()

    def get_following(self, obj):
        return obj.following.count()


class UserInformationSerializer(UserSmallInformationSerializer):
    posts = serializers.SerializerMethodField()
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name',  'followers', 'following', 'profile', 'posts']
        read_only_fields = ['username', 'id', 'posts', 'followers', 'following', 'profile']

    def get_posts(self, obj):
        posts = Post.objects.filter(author=obj)
        request = self.context.get('request')
        return PostListCreateSerializer(posts, many=True, context={'request': request}).data

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)
        profile = instance.profile
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        if profile_data:
            profile.bio = profile_data.get('bio', profile.bio)
            profile.birth_date = profile_data.get('birth_date', profile.birth_date)
            profile.profile_pic = profile_data.get('profile_pic', profile.profile_pic)
            profile.save()
        return instance


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords don't match."})
        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Old password is incorrect')
        return value


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = '__all__'
        read_only_fields = ['id', 'follower', 'following', 'created_at']
