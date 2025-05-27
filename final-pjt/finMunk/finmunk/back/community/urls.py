from django.urls import path
from . import views

urlpatterns = [
    # 게시글
    path('articles/', views.article_list, name='article-list'),
    path('articles/<int:article_pk>/', views.article_detail, name='article-detail'),
    path('articles/<int:article_pk>/like/', views.toggle_article_like, name='article-like'),
    path('articles/liked/', views.liked_articles, name='liked-articles'),
    path('articles/popular/', views.top_liked_articles, name='top-liked-articles'),


    # 댓글
    path('comments/', views.comment_list, name='comment-list'),
    path('comments/<int:comment_pk>/', views.comment_detail, name='comment-detail'),
    path('comments/<int:comment_pk>/like/', views.toggle_comment_like, name='comment-like'),

    # 알림
    path('notifications/', views.my_notifications, name='my-notifications'),
    path('notifications/<int:pk>/read/', views.mark_notification_as_read, name='notification-read'),
]
