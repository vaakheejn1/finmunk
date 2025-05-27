# community/models.py

from django.db import models
from django.conf import settings

class Article(models.Model):
    CATEGORY_CHOICES = [
    ('notice', '공지사항'),
    ('event', '이벤트'),
    ('tip', '자유게시판'),
]

    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='tip')
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    liked_by = models.ManyToManyField('users.User', related_name='liked_articles', blank=True)
    image = models.ImageField(upload_to='article_images/', blank=True, null=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    liked_by = models.ManyToManyField('users.User', related_name='liked_comments', blank=True)

    def __str__(self):
        return f"{self.user.username}의 댓글"

# models.py
class Notification(models.Model):
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    message = models.TextField()
    url = models.CharField(max_length=255, blank=True)  # 클릭 시 이동할 주소 (예: 게시글 상세)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"To {self.recipient.username}: {self.message}"



