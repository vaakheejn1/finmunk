from django.urls import path
from .views import product_summary_api

urlpatterns = [
    path('summary/', product_summary_api),
]