from django.urls import path
from . import views

urlpatterns = [
    # path('profile/<username>/', UserProfileView.as_view(), name='user-profile'),
    path('profile/', views.profile, name='user-profile'),
    path('profile/<int:user_id>/', views.user_profile, name='user-profile-detail'),
    path('delete/', views.delete_user, name='delete-user'),
    path('follow/<int:user_id>/', views.toggle_follow, name='toggle-follow'),
]
