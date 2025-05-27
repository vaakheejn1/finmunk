from django.contrib import admin
from .models import Consultation

@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_age', 'product_name', 'phone', 'created_at')  # ← 추가
    search_fields = ('user__username', 'product_name', 'phone')

    def user_age(self, obj):
        return obj.user.age
    user_age.short_description = '나이'

