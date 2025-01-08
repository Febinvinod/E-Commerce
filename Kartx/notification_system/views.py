# notifications/views.py
from django.http import JsonResponse
from .send_email import send_email
from .models import payment_data  # Here We are using Dummy Data , After we are receiving data from the direct payment section we can integrate it directly.

def send_notifications(request, payment_id):
    # Fetch user info from the payment data (for demo purposes)
    user_info = next((user for user in payment_data if user["payment_id"] == payment_id), None)

    if user_info:
        # Trigger email notification
        send_email(user_info)
        return JsonResponse({"message": "Email notification sent successfully!"})
    else:
        return JsonResponse({"message": "Payment ID not found."}, status=404)
