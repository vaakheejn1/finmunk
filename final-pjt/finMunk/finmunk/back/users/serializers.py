# back/users/serializers.py
from community.models import Article, Comment  # 네 구조에 맞게 import
from rest_framework import serializers
from .models import User 
from dj_rest_auth.registration.serializers import RegisterSerializer
from .models import *
from django.contrib.auth import get_user_model
from dj_rest_auth.serializers import UserDetailsSerializer

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()
    followings_count = serializers.SerializerMethodField()
    is_following = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'age', 'job', 'income', 'assets', 'profile_image',
                  'followers_count', 'followings_count', 'is_following', 'bio']

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_followings_count(self, obj):
        return obj.followings.count()

    def get_is_following(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return request.user in obj.followers.all()
        return False


class CustomUserDetailSerializer(UserDetailsSerializer):
    class Meta:
        extra_fields = []
        if hasattr(UserModel, 'USERNAME_FIELD'):
            extra_fields.append(UserModel.USERNAME_FIELD)
        if hasattr(UserModel, 'EMAIL_FIELD'):
            extra_fields.append(UserModel.EMAIL_FIELD)
        if hasattr(UserModel, 'first_name'):
            extra_fields.append('first_name')
        if hasattr(UserModel, 'last_name'):
            extra_fields.append('last_name')
        # if hasattr(UserModel, 'nickname'):
        #     extra_fields.append('nickname')
        if hasattr(UserModel, 'age'):
            extra_fields.append('age')
        if hasattr(UserModel, 'assets'):
            extra_fields.append('assets')
        if hasattr(UserModel, 'job'):
            extra_fields.append('job')
        if hasattr(UserModel, 'income'):
            extra_fields.append('income')
        model = UserModel
        fields = ('pk', *extra_fields)
        read_only_fields = ('email',)

# 회원가입용 커스텀 시리얼라이저
class CustomRegisterSerializer(RegisterSerializer):
    age = serializers.IntegerField(required=False, allow_null=True)
    job = serializers.BooleanField(required=False, default=False)  # Boolean으로 변경
    income = serializers.IntegerField(required=False, allow_null=True)
    assets = serializers.IntegerField(required=False, allow_null=True)

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['age'] = self.validated_data.get('age', None)
        data['job'] = self.validated_data.get('job', False)
        data['income'] = self.validated_data.get('income', None)
        data['assets'] = self.validated_data.get('assets', None)
        return data

    def save(self, request):
        user = super().save(request)
        user.age = self.get_cleaned_data().get('age')
        user.job = self.get_cleaned_data().get('job')
        user.income = self.get_cleaned_data().get('income')
        user.assets = self.get_cleaned_data().get('assets')
        user.save()
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()
    followings_count = serializers.SerializerMethodField()
    articles = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    is_following = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'profile_image',
            'age', 'job', 'income', 'assets',  
            'followers_count', 'followings_count',
            'articles', 'comments', 'is_following', 'bio',
        ]

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_followings_count(self, obj):
        return obj.followings.count()

    def get_articles(self, obj):
        return [{'id': article.id, 'title': article.title} for article in Article.objects.filter(user=obj)]

    def get_comments(self, obj):
        comments = Comment.objects.filter(user=obj).select_related('article', 'user') 

        return [{
            'id': c.id,
            'content': c.content[:30],
            'article': c.article.id,
            'user': {
                'id': c.user.id,  
                'username': c.user.username
            }
        } for c in comments]


    def get_is_following(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.followers.filter(id=request.user.id).exists()
        return False



    