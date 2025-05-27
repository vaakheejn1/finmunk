# back/products/models.py
from django.db import models
from django.conf import settings

class DepositProduct(models.Model):
    bank_name = models.CharField(max_length=50)
    product_name = models.CharField(max_length=100)
    join_way = models.TextField()
    maturity_type = models.TextField(blank=True, null=True)
    join_deny = models.CharField(max_length=10)
    max_limit = models.CharField(max_length=50, blank=True, null=True)
    save_term = models.CharField(max_length=10)
    interest_rate = models.FloatField()
    interest_rate2 = models.FloatField(blank=True, null=True)
    liked_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_deposits', blank=True)

    def __str__(self):
        return f"{self.product_name} ({self.bank_name})"

class SavingProduct(models.Model):
    bank_name = models.CharField(max_length=50)
    product_name = models.CharField(max_length=100)
    join_way = models.TextField()
    maturity_type = models.TextField(blank=True, null=True)
    join_deny = models.CharField(max_length=10)
    max_limit = models.CharField(max_length=50, blank=True, null=True)
    save_term = models.CharField(max_length=10)
    interest_rate = models.FloatField()
    interest_rate2 = models.FloatField(blank=True, null=True)
    liked_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_savings', blank=True)

    def __str__(self):
        return f"{self.product_name} ({self.bank_name})"

# class Favorite(models.Model):
#     user = models.ForeignKey('users.User', on_delete=models.CASCADE)
#     product_type = models.CharField(max_length=10)  # 'deposit' or 'saving'
#     product_id = models.IntegerField()

#     def __str__(self):
#         return f"{self.user.username} → {self.product_type}:{self.product_id}"

