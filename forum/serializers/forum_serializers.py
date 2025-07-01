# forum/serializers/forum_serializers.py

from rest_framework import serializers
from forum.models import Category, Post, Comment, Reply
from django.contrib.auth import get_user_model

User = get_user_model()

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class ReplySerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)
    time_since_replied = serializers.SerializerMethodField()

    class Meta:
        model = Reply
        fields = ['id', 'comment', 'author', 'author_username', 'content', 'created_at', 'updated_at', 'time_since_replied']
        read_only_fields = ['author', 'created_at', 'updated_at'] # Author will be set by the view

    def get_time_since_replied(self, obj):
        return obj.time_since_replied()

class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)
    replies = ReplySerializer(many=True, read_only=True) # Nested replies
    time_since_commented = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'author_username', 'content', 'created_at', 'updated_at', 'replies', 'time_since_commented']
        read_only_fields = ['author', 'created_at', 'updated_at'] # Author will be set by the view

    def get_time_since_commented(self, obj):
        return obj.time_since_commented()

class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    comments = CommentSerializer(many=True, read_only=True) # Nested comments
    comment_count = serializers.SerializerMethodField() # To show total comments
    time_since_posted = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'author', 'author_username', 'category', 'category_name', 'title', 'details', 'created_at', 'updated_at', 'comments', 'comment_count', 'time_since_posted']
        read_only_fields = ['author', 'created_at', 'updated_at'] # Author will be set by the view

    def get_comment_count(self, obj):
        return obj.comments.count()

    def get_time_since_posted(self, obj):
        return obj.time_since_posted()