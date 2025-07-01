# forum/urls.py

from django.urls import path
from forum.views import forum_views

urlpatterns = [
    # Category Endpoints
    path('categories/', forum_views.CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', forum_views.CategoryDetailView.as_view(), name='category-detail'),

    # Post Endpoints
    path('posts/', forum_views.PostListCreateView.as_view(), name='post-list-create'),
    path('posts/<int:pk>/', forum_views.PostDetailView.as_view(), name='post-detail'),
    path('posts/my-posts/', forum_views.MyPostListView.as_view(), name='my-posts'),
    path('posts/category/<int:category_id>/', forum_views.PostsByCategoryListView.as_view(), name='posts-by-category'),

    # Comment Endpoints
    path('posts/<int:post_id>/comments/', forum_views.CommentListCreateView.as_view(), name='comment-list-create'),
    path('comments/<int:pk>/', forum_views.CommentDetailView.as_view(), name='comment-detail'),

    # Reply Endpoints
    path('comments/<int:comment_id>/replies/', forum_views.ReplyListCreateView.as_view(), name='reply-list-create'),
    path('replies/<int:pk>/', forum_views.ReplyDetailView.as_view(), name='reply-detail'),
]

