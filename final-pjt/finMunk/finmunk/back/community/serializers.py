from rest_framework import serializers
from .models import Article, Comment, Notification
from users.serializers import UserSerializer

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True) 
    like_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'user', 'article', 'content', 'created_at', 'like_count', 'is_liked']
        read_only_fields = ['id', 'user', 'created_at', 'like_count', 'is_liked']

    def get_like_count(self, obj):
        return obj.liked_by.count()

    def get_is_liked(self, obj):
        user = self.context.get('request').user
        return user.is_authenticated and obj.liked_by.filter(id=user.id).exists()


class ArticleSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True) 
    comment_count = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    category = serializers.CharField()
    image = serializers.ImageField(required=False)

    class Meta:
        model = Article
        fields = [
            'id', 'user', 'title', 'content', 'category', 'image',
            'created_at', 'comment_count', 'like_count', 'is_liked'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'comment_count', 'like_count', 'is_liked']


    def get_comment_count(self, obj):
        return obj.comment_set.count()

    def get_like_count(self, obj):
        return obj.liked_by.count()

    def get_is_liked(self, obj):
        user = self.context.get('request').user
        return user.is_authenticated and obj.liked_by.filter(id=user.id).exists()

class NotificationSerializer(serializers.ModelSerializer):
    recipient = serializers.StringRelatedField(read_only=True)  

    class Meta:
        model = Notification
        fields = ['id', 'message', 'url', 'is_read', 'created_at', 'recipient']

