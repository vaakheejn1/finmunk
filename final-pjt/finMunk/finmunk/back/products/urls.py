from django.urls import path
from .views import (
    RecommendProductAPIView,
    DepositProductListView,
    SavingProductListView,
    AllProductsAPIView,
    toggle_deposit_like, 
    toggle_saving_like,
    liked_products,      
)

urlpatterns = [
    path('recommend/', RecommendProductAPIView.as_view(), name='recommend-products'),
    path('deposits/', DepositProductListView.as_view(), name='deposit-list'),
    path('savings/', SavingProductListView.as_view(), name='saving-list'),
    path('all-products/', AllProductsAPIView.as_view(), name='all-products'),
    path('toggle-deposit-like/<int:product_id>/', toggle_deposit_like, name='toggle-deposit-like'),
    path('toggle-saving-like/<int:product_id>/', toggle_saving_like, name='toggle-saving-like'),
    path('liked-products/', liked_products, name='liked-products'),
]
