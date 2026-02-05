from celery import shared_task
from django.core.mail import send_mail

from .models import Order


@shared_task
def send_order_confirmation(order_id):

    try:
        order = Order.objects.get(id=order_id)

        # Fake email 
        subject = "Order Confirmation"
        message = f"Your order {order.id} is {order.status}"

        send_mail(
            subject,
            message,
            "noreply@test.com",
            ["user@test.com"],
            fail_silently=True
        )

        return "Email sent"

    except Order.DoesNotExist:
        return "Order not found"
