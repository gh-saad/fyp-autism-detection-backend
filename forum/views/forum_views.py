# forum/views/forum_views.py

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import PermissionDenied
from forum.models import Category, Post, Comment, Reply
from forum.serializers.forum_serializers import (
    CategorySerializer,
    PostSerializer,
    CommentSerializer,
    ReplySerializer
)
from forum.services.forum_service import ForumService

# --- Category Views ---
class CategoryListCreateView(generics.ListCreateAPIView):
    """
    List all categories or create a new category.
    Only authenticated users can create categories.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated] # Or IsAdminUser if only admins can create categories

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()] # Anyone can view categories
        return [IsAuthenticated()] # Only authenticated users can create
        
class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a category.
    Only authenticated users (or admins) can update/delete.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated] # Or IsAdminUser

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()] # Anyone can view a category
        return [IsAuthenticated()] # Only authenticated users can update/delete


# --- Post Views ---
class PostListCreateView(generics.ListCreateAPIView):
    """
    List all forum posts or create a new post.
    Authenticated users can create posts.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = []

    def perform_create(self, serializer):
        # Set the author of the post to the current authenticated user
        serializer.save(author=self.request.user)

    def get_queryset(self):
        # Optionally filter posts by category if a category_id is provided in query params
        queryset = super().get_queryset()
        category_id = self.request.query_params.get('category_id', None)
        if category_id is not None:
            queryset = queryset.filter(category_id=category_id)
        return queryset.select_related('author', 'category').prefetch_related('comments__author', 'comments__replies__author')


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a forum post.
    Only the author can update/delete their own post.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        obj = super().get_object()
        # Ensure only the author can update/delete
        if self.request.method in ['PUT', 'PATCH', 'DELETE'] and obj.author != self.request.user:
            raise PermissionDenied("You do not have permission to perform this action on this post.")
        return obj

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()


class MyPostListView(generics.ListAPIView):
    """
    List all posts created by the currently authenticated user.
    """
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter posts by the current authenticated user
        return Post.objects.filter(author=self.request.user).select_related('author', 'category').prefetch_related('comments__author', 'comments__replies__author')

class PostsByCategoryListView(generics.ListAPIView):
    """
    List all posts belonging to a specific category.
    """
    serializer_class = PostSerializer
    permission_classes = [AllowAny] # Anyone can view posts by category

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        return Post.objects.filter(category_id=category_id).select_related('author', 'category').prefetch_related('comments__author', 'comments__replies__author')


# --- Comment Views ---
class CommentListCreateView(generics.ListCreateAPIView):
    """
    List all comments for a specific post or create a new comment.
    Authenticated users can create comments.
    """
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Comment.objects.filter(post_id=post_id).select_related('author').prefetch_related('replies__author')

    def perform_create(self, serializer):
        post = generics.get_object_or_404(Post, id=self.kwargs['post_id'])
        serializer.save(author=self.request.user, post=post)

class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a comment.
    Only the author can update/delete their own comment.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        obj = super().get_object()
        if self.request.method in ['PUT', 'PATCH', 'DELETE'] and obj.author != self.request.user:
            raise PermissionDenied("You do not have permission to perform this action on this comment.")
        return obj

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()


# --- Reply Views ---
class ReplyListCreateView(generics.ListCreateAPIView):
    """
    List all replies for a specific comment or create a new reply.
    Authenticated users can create replies.
    """
    serializer_class = ReplySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        comment_id = self.kwargs['comment_id']
        return Reply.objects.filter(comment_id=comment_id).select_related('author')

    def perform_create(self, serializer):
        comment = generics.get_object_or_404(Comment, id=self.kwargs['comment_id'])
        serializer.save(author=self.request.user, comment=comment)

class ReplyDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a reply.
    Only the author can update/delete their own reply.
    """
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        obj = super().get_object()
        if self.request.method in ['PUT', 'PATCH', 'DELETE'] and obj.author != self.request.user:
            raise PermissionDenied("You do not have permission to perform this action on this reply.")
        return obj

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()
