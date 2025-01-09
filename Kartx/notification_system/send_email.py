# notifications/send_email.py
from django.core.mail import send_mail
from django.conf import settings

def send_email(user_info):
    subject = 'Order Status Update'
    message = (
        f"Hello {user_info['user_name']},\n\n"
        f"Your order with Order ID {user_info['order_id']} has been updated to the following status: {user_info['status']}.\n\n"
        f"Thank you for shopping with us."
    )
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user_info['email']]  # User's email address

    # Send the email via SMTP
    try:
        send_mail(subject, message, from_email, recipient_list)
        print(f"Email sent to {user_info['email']}")
    except Exception as e:
        print(f"Error sending email: {e}")
