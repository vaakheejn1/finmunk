# financial/serializers.py
from rest_framework import serializers
from .models import DepositProduct, SavingProduct

class RecommendationRequestSerializer(serializers.Serializer):
    age = serializers.IntegerField()
    job = serializers.IntegerField()
    monthly_income = serializers.IntegerField()
    assets = serializers.IntegerField()

class DepositProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositProduct
        fields = '__all__'

class SavingProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingProduct
        fields = '__all__'
