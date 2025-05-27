from django.urls import path
from . import views

app_name = 'videos'

urlpatterns = [
    path('', views.youtube_search, name='youtube_search'),        
    path('saved/', views.saved_videos, name='saved_videos'),     
    path('save/', views.save_or_delete_video, name='save_video'),
    path('stock-summary/', views.stock_summary_for_video, name='stock_summary_for_video'), 
    path('summarize-video/', views.summarize_video_by_id),
]
