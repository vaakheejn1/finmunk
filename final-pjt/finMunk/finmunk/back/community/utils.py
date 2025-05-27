# utils.py
from .models import Notification
from django.contrib.auth import get_user_model

User = get_user_model()

def create_mention_notifications(content, actor_user, article):
    import re
    mentioned_usernames = set(re.findall(r'@([\w]+)', content))
    for username in mentioned_usernames:
        try:
            recipient = User.objects.get(username=username)
            if recipient != actor_user:
                Notification.objects.create(
                    recipient=recipient,
                    message=f"💬 @{actor_user.username}님이 당신을 언급했어요!",
                    url=f"/community/articles/{article.id}/"
                )
        except User.DoesNotExist:
            continue

def create_article_like_notification(user, article):
    if user != article.user:
        Notification.objects.create(
            recipient=article.user,
            message=f"❤️ @{user.username}님이 게시글을 좋아요했어요!",
            url=f"/community/articles/{article.id}/"
        )

def create_comment_like_notification(user, comment):
    if user != comment.user:
        Notification.objects.create(
            recipient=comment.user,
            message=f"👍 @{user.username}님이 댓글을 좋아요했어요!",
            url=f"/community/articles/{comment.article.id}/"
        )

def create_comment_notification(user, article):
    if user != article.user:
        Notification.objects.create(
            recipient=article.user,
            message=f"💬 @{user.username}님이 내 게시글에 댓글을 달았어요!",
            url=f"/community/articles/{article.id}/"
        )

def create_notice_event_notification(article):
    print("✅ 공지/이벤트 알림 생성 시작")
    print("✅ 대상 게시글 ID:", article.id)
    print("✅ 카테고리:", article.category)

    label_map = {
        'notice': '공지사항',
        'event': '이벤트'
    }
    label = label_map.get(article.category, '공지')

    users = User.objects.all()
    print(f" 전체 유저 수: {users.count()}")

    for user in users:
        print(f"🔔 알림 대상 유저: {user.username}")
        Notification.objects.create(
            recipient=user,
            message=f"📢 새로운 {label}이 등록되었어요!",
            url=f"/community/articles/{article.id}/"
        )
    print(" 공지/이벤트 알림 생성 완료")

def create_follow_notification(from_user, to_user):
    if from_user != to_user:
        Notification.objects.create(
            recipient=to_user,
            message=f"👥 @{from_user.username}님이 당신을 팔로우했어요!",
            url=f"/profile/{from_user.id}/"
        )

def create_following_article_notification(article):
    author = article.user
    followers = author.followers.all()  # 나를 팔로우하는 사람들(X), 내가 팔로우한 사람들(O)

    for follower in followers:
        if follower != author:
            Notification.objects.create(
                recipient=follower,
                message=f"✍️ @{author.username}님이 새 글을 작성했어요!",
                url=f"/community/articles/{article.id}/"
            )


