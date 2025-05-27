from django.contrib import admin
from .models import DepositProduct, SavingProduct

@admin.register(DepositProduct)
class DepositProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'bank_name')
    filter_horizontal = ('liked_by',)  # ManyToManyField 보기 쉽게!

@admin.register(SavingProduct)
class SavingProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'bank_name')
    filter_horizontal = ('liked_by',)
