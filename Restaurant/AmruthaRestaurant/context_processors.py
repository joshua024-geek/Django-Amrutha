from .models import Cart, Notification


def cart_item_count(request):
  user_id = request.session.get('user_id')
  if user_id:
        count = Cart.objects.filter(user_id=user_id, status='pending').count()
        return {'cart_item_count': count}
  return {'cart_item_count': 0}


def admin_notifications_count(request):
    user_id = request.session.get('user_id')
    if user_id:
      unread_admin_count = Notification.objects.filter(read_status=False).count()
      return {'unread_admin_count': unread_admin_count}
    return {'unread_admin_count': 0}




def customer_notifications_count(request):
    user_id = request.session.get('user_id')
    if user_id:
      unread_customer_count = Notification.objects.filter(customer_read_status=False).count()
      return {'unread_customer_count': unread_customer_count}
    return {'unread_customer_count': 0}