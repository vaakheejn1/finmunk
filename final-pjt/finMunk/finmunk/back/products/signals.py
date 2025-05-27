from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import DepositProduct, SavingProduct
from community.models import Notification
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.mail import send_mail
User = get_user_model()


def send_interest_email(user, product_name, old_rate, new_rate):
    subject = f"[FINMUNK] '{product_name}' 금리 변경 안내"
    message = (
        f"{user.username}님 안녕하세요!\n\n"
        f"'{product_name}' 상품의 금리가 다음과 같이 변경되었습니다:\n"
        f"👉 {old_rate}% → {new_rate}%\n\n"
        f"지금 확인해보세요!\n\n"
        "📌 바로가기: https://finmunk.com/compare\n\n"
        "감사합니다. - FINMUNK 🐿️"
    )
    recipient = [user.email]

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        recipient,
        fail_silently=False,
    )


@receiver(pre_save, sender=DepositProduct)
def notify_interest_change_deposit(sender, instance, **kwargs):
    try:
        original = DepositProduct.objects.get(pk=instance.pk)
    except DepositProduct.DoesNotExist:
        return

    if original.interest_rate != instance.interest_rate:
        for user in instance.liked_by.all():
            Notification.objects.create(
                recipient=user,
                message=f"💸 '{instance.product_name}' 상품의 금리가 변경되었어요! ({original.interest_rate} → {instance.interest_rate}%)",
                url="/compare"
            )
            send_interest_email(user, instance.product_name, original.interest_rate, instance.interest_rate)

@receiver(pre_save, sender=SavingProduct)
def notify_interest_change_saving(sender, instance, **kwargs):
    try:
        original = SavingProduct.objects.get(pk=instance.pk)
    except SavingProduct.DoesNotExist:
        return

    if original.interest_rate != instance.interest_rate:
        for user in instance.liked_by.all():
            Notification.objects.create(
                recipient=user,
                message=f"💸 '{instance.product_name}' 적금 상품의 금리가 변경되었어요! ({original.interest_rate} → {instance.interest_rate}%)",
                url="/compare"
            )
            send_interest_email(user, instance.product_name, original.interest_rate, instance.interest_rate)
