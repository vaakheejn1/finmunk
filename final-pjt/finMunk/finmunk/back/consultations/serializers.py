from rest_framework import serializers
from .models import Consultation

class ConsultationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consultation
        fields = ['id', 'user', 'product_name', 'phone', 'created_at']
        read_only_fields = ['user', 'created_at']
