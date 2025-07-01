# forum/services/forum_service.py

from forum.models import Category, Post, Comment, Reply
from django.shortcuts import get_object_or_404
from django.db.models import Count

class ForumService:
    @staticmethod
    def get_all_categories():
        return Category.objects.all()

    @staticmethod
    def get_category_by_id(category_id):
        return get_object_or_404(Category, id=category_id)

    @staticmethod
    def create_category(name, description=None):
        return Category.objects.create(name=name, description=description)

    @staticmethod
    def update_category(category_id, name=None, description=None):
        category = get_object_or_404(Category, id=category_id)
        if name:
            category.name = name
        if description is not None: # Allow setting to empty string
            category.description = description
        category.save()
        return category

    @staticmethod
    def delete_category(category_id):
        category = get_object_or_404(Category, id=category_id)
        category.delete()
        return True

    @staticmethod
    def get_all_posts(category_id=None):
        if category_id:
            return Post.objects.filter(category_id=category_id).select_related('author', 'category').prefetch_related('comments__author', 'comments__replies__author')
        return Post.objects.all().select_related('author', 'category').prefetch_related('comments__author', 'comments__replies__author')

    @staticmethod
    def get_post_by_id(post_id):
        return get_object_or_404(Post.objects.select_related('author', 'category').prefetch_related('comments__author', 'comments__replies__author'), id=post_id)

    @staticmethod
    def create_post(author, category_id, title, details):
        category = get_object_or_404(Category, id=category_id)
        return Post.objects.create(author=author, category=category, title=title, details=details)

    @staticmethod
    def update_post(post_id, author, title=None, details=None, category_id=None):
        post = get_object_or_404(Post, id=post_id, author=author) # Ensure only author can update their post
        if title:
            post.title = title
        if details:
            post.details = details
        if category_id:
            category = get_object_or_404(Category, id=category_id)
            post.category = category
        post.save()
        return post

    @staticmethod
    def delete_post(post_id, author):
        post = get_object_or_404(Post, id=post_id, author=author) # Ensure only author can delete their post
        post.delete()
        return True

    @staticmethod
    def get_posts_by_author(author):
        return Post.objects.filter(author=author).select_related('author', 'category').prefetch_related('comments__author', 'comments__replies__author')

    @staticmethod
    def get_comments_for_post(post_id):
        post = get_object_or_404(Post, id=post_id)
        return post.comments.all().select_related('author').prefetch_related('replies__author')

    @staticmethod
    def get_comment_by_id(comment_id):
        return get_object_or_404(Comment.objects.select_related('author').prefetch_related('replies__author'), id=comment_id)

    @staticmethod
    def create_comment(post_id, author, content):
        post = get_object_or_404(Post, id=post_id)
        return Comment.objects.create(post=post, author=author, content=content)

    @staticmethod
    def update_comment(comment_id, author, content):
        comment = get_object_or_404(Comment, id=comment_id, author=author) # Only author can update
        comment.content = content
        comment.save()
        return comment

    @staticmethod
    def delete_comment(comment_id, author):
        comment = get_object_or_404(Comment, id=comment_id, author=author) # Only author can delete
        comment.delete()
        return True

    @staticmethod
    def get_replies_for_comment(comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        return comment.replies.all().select_related('author')

    @staticmethod
    def get_reply_by_id(reply_id):
        return get_object_or_404(Reply.objects.select_related('author'), id=reply_id)

    @staticmethod
    def create_reply(comment_id, author, content):
        comment = get_object_or_404(Comment, id=comment_id)
        return Reply.objects.create(comment=comment, author=author, content=content)

    @staticmethod
    def update_reply(reply_id, author, content):
        reply = get_object_or_404(Reply, id=reply_id, author=author) # Only author can update
        reply.content = content
        reply.save()
        return reply

    @staticmethod
    def delete_reply(reply_id, author):
        reply = get_object_or_404(Reply, id=reply_id, author=author) # Only author can delete
        reply.delete()
        return True
