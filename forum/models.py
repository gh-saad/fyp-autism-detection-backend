# forum/models.py

from django.db import models
from django.conf import settings # To get AUTH_USER_MODEL
from django.utils import timezone
from datetime import timedelta

# Get the custom User model defined in settings.AUTH_USER_MODEL
User = settings.AUTH_USER_MODEL

class Category(models.Model):
    """
    Represents a category for forum posts.
    E.g., "General Parenting", "Behavior Support", "Autism Journey"
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

class Post(models.Model):
    """
    Represents a discussion post in the forum.
    """
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='forum_posts')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='posts')
    title = models.CharField(max_length=255)
    details = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at'] # Order by newest first

    def __str__(self):
        return self.title

    def time_since_posted(self):
        """
        Returns a human-readable string indicating how long ago the post was made.
        """
        now = timezone.now()
        diff = now - self.created_at

        seconds = int(diff.total_seconds())
        if seconds < 60:
            return f"{seconds} seconds ago"
        minutes = seconds // 60
        if minutes < 60:
            return f"{minutes} minutes ago"
        hours = minutes // 60
        if hours < 24:
            return f"{hours} hours ago"
        days = hours // 24
        if days < 30:
            return f"{days} days ago"
        months = days // 30 # Approximate
        if months < 12:
            return f"{months} months ago"
        years = days // 365 # Approximate
        return f"{years} years ago"


class Comment(models.Model):
    """
    Represents a comment on a forum post.
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='forum_comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at'] # Order by oldest first

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"

    def time_since_commented(self):
        """
        Returns a human-readable string indicating how long ago the comment was made.
        """
        now = timezone.now()
        diff = now - self.created_at

        seconds = int(diff.total_seconds())
        if seconds < 60:
            return f"{seconds} seconds ago"
        minutes = seconds // 60
        if minutes < 60:
            return f"{minutes} minutes ago"
        hours = minutes // 60
        if hours < 24:
            return f"{hours} hours ago"
        days = hours // 24
        if days < 30:
            return f"{days} days ago"
        months = days // 30 # Approximate
        if months < 12:
            return f"{months} months ago"
        years = days // 365 # Approximate
        return f"{years} years ago"


class Reply(models.Model):
    """
    Represents a reply to a comment.
    """
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='forum_replies')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at'] # Order by oldest first
        verbose_name_plural = "Replies"

    def __str__(self):
        return f"Reply by {self.author.username} on comment by {self.comment.author.username}"

    def time_since_replied(self):
        """
        Returns a human-readable string indicating how long ago the reply was made.
        """
        now = timezone.now()
        diff = now - self.created_at

        seconds = int(diff.total_seconds())
        if seconds < 60:
            return f"{seconds} seconds ago"
        minutes = seconds // 60
        if minutes < 60:
            return f"{minutes} minutes ago"
        hours = minutes // 60
        if hours < 24:
            return f"{hours} hours ago"
        days = hours // 24
        if days < 30:
            return f"{days} days ago"
        months = days // 30 # Approximate
        if months < 12:
            return f"{months} months ago"
        years = days // 365 # Approximate
        return f"{years} years ago"