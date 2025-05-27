from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    ## 로그인/회원가입
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('dj_rest_auth.urls')),  # 로그인/로그아웃
    path('api/v1/auth/registration/', include('dj_rest_auth.registration.urls')),  # 회원가입

    ## 사용자 관련 (여기만 수정!)
    path('api/v1/users/', include('users.urls')),  # 사용자 프로필로 분리

    ## 커뮤니티
    path('api/v1/community/', include('community.urls')),

    ## 상품정보, 추천
    path('api/v1/products/', include('products.urls')),

    ## 주식정보
    path('api/v1/videos/', include('videos.urls')),

    ## 금융정보
    path('api/v1/market/', include('market.urls')),

    ## 챗봇
    path('api/v1/chatbot/', include('chatbot.urls')),

    path('api/v1/consultations/', include('consultations.urls')),

    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)