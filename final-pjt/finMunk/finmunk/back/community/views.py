from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from .models import Article, Comment, Notification
from .serializers import ArticleSerializer, CommentSerializer, NotificationSerializer
from .utils import (
    create_mention_notifications,
    create_article_like_notification,
    create_comment_like_notification,
    create_comment_notification,
    create_notice_event_notification,
    create_following_article_notification,
)

# 게시글 목록, 작성
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def article_list(request):
    if request.method == 'GET':
        category = request.GET.get('category')
        articles = Article.objects.all().order_by('-created_at')
        if category:
            articles = articles.filter(category=category)
        serializer = ArticleSerializer(articles, many=True, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'POST':
        req_category = request.data.get('category')
        if req_category in ['notice', 'event']:
            if not request.user.is_staff:
                return Response({'detail': '공지/이벤트는 관리자만 작성할 수 있어요!'}, status=403)

        serializer = ArticleSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            article = serializer.save(user=request.user)

            # ✅ 공지/이벤트면 전체 알림
            if req_category in ['notice', 'event']:
                create_notice_event_notification(article)

            # ✅ 팔로워에게 알림
            create_following_article_notification(article)

            return Response(serializer.data, status=201)


from django.db.models import Count
from rest_framework.permissions import AllowAny

@api_view(['GET'])
@permission_classes([AllowAny])
def top_liked_articles(request):
    top_articles = Article.objects.annotate(
        like_count=Count('liked_by')
    ).order_by('-like_count', '-created_at')[:5]

    serializer = ArticleSerializer(top_articles, many=True, context={'request': request})
    return Response(serializer.data)


# 게시글 상세        
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def article_detail(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)

    if request.method == 'GET':
        serializer = ArticleSerializer(article, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'PUT':
        if article.user != request.user:
            return Response({'detail': '수정 권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = ArticleSerializer(article, data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    elif request.method == 'DELETE':
        if article.user != request.user:
            return Response({'detail': '삭제 권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)

        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# 댓글 목록, 작성
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def comment_list(request):
    if request.method == 'GET':
        article_id = request.GET.get('article')
        if article_id:
            comments = Comment.objects.filter(article__id=article_id).order_by('created_at')
        else:
            comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True, context={'request': request}) 
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CommentSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            comment = serializer.save(user=request.user)

            # 알림: 언급
            create_mention_notifications(comment.content, request.user, comment.article)

            # 알림: 댓글 달림
            create_comment_notification(request.user, comment.article)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

# 댓글 수정 삭제 
@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def comment_detail(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)

    if request.method == 'PUT':
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    elif request.method == 'DELETE':
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# 게시글 좋아요
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_article_like(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    user = request.user

    if user in article.liked_by.all():
        article.liked_by.remove(user)
    else:
        article.liked_by.add(user)
        create_article_like_notification(user, article)

    serializer = ArticleSerializer(article, context={'request': request})
    return Response(serializer.data, status=200)

# 댓글 좋아요
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_comment_like(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    user = request.user

    if user in comment.liked_by.all():
        comment.liked_by.remove(user)
    else:
        comment.liked_by.add(user)
        create_comment_like_notification(user, comment)

    serializer = CommentSerializer(comment, context={'request': request})
    return Response(serializer.data, status=200)

# 좋아요한 게시글 목록
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def liked_articles(request):
    user = request.user
    articles = user.liked_articles.all().order_by('-created_at')
    serializer = ArticleSerializer(articles, many=True, context={'request': request})
    return Response(serializer.data)

# 내 알림 목록
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_notifications(request):
    notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    serializer = NotificationSerializer(notifications, many=True)
    return Response(serializer.data)

# 알림 읽음 처리
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_notification_as_read(request, pk):
    notification = get_object_or_404(Notification, pk=pk, recipient=request.user)
    notification.is_read = True
    notification.save()
    return Response({'message': '읽음 처리 완료'})
