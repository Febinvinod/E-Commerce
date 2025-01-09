# notifications/views.py
from django.http import JsonResponse
from .send_email import send_email
from .models import payment_data  # Importing the dummy data

def send_notifications(request, payment_id):
    # Fetch user info from the payment data (for demo purposes)
    user_info = next((user for user in payment_data if user["payment_id"] == payment_id), None)

    if user_info:
        # Optional: Update the status based on the request (assuming a status query parameter)
        new_status = request.GET.get('status')
        if new_status:
            if new_status in ["Packing", "Despatched", "On-way", "Delivered"]:
                user_info['status'] = new_status
            else:
                return JsonResponse({"message": "Invalid status."}, status=400)

        # Trigger email notification
        send_email(user_info)
        return JsonResponse({"message": "Email notification sent successfully!"})
    else:
        return JsonResponse({"message": "Payment ID not found."}, status=404)
