from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Root URL to load index.html
    path('about/', views.about, name='about'),
    path('menu/', views.foodmenu, name='foodmenu'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('customerdashboard/', views.customerdashboard, name='customerdashboard'),
    path('logout/', views.logout, name='logout'),
    path('adminlogout/', views.adminlogout, name='adminlogout'),
    path('adminsignin/', views.adminsignin, name='adminsignin'),
    path('admindashboard/', views.admindashboard, name='admindashboard'),
    path('customermenu/', views.customermenu, name='customermenu'),
    path('customer_list/', views.customer_list, name='customer_list'),  # URL for the customer list page
    path('menu_items/', views.menu_items, name='menu_items'),
    path('add_item/', views.add_item, name='add_item'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='cart'),
    path('remove_item/<int:item_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('checkout/', views.checkout, name='checkout'),
    path('place_order/', views.place_order, name='place_order'),
    path('order/<str:order_number>/', views.order_details, name='order_details'),
    path('order_success/', views.order_success, name='order_success'),
    path('customer_orders/<str:order_number>/', views.admin_order_details, name='admin_order_details'),
    path('admin_profile/', views.admin_profile, name='admin_profile'),
    path('customer_profile/', views.customer_profile, name='customer_profile'),
    path('order/<str:order_number>/mark-processing/', views.mark_order_processing, name='mark_order_processing'),
    path('order/<str:order_number>/mark-delivered/', views.mark_order_delivered, name='mark_order_delivered'),
    path('block_user/<int:user_id>/', views.block_user, name='block_user'),
    path('unblock_user/<int:user_id>/', views.unblock_user, name='unblock_user'),
    path('menu/edit/<int:item_id>/', views.edit_item, name='edit_item'),
    path('menu_items/delete/<int:item_id>/', views.delete_item, name='delete_item'),
    path('admin_notifications/', views.admin_notifications_view, name='admin_notifications'),
    path('customer_notifications/', views.customer_notifications_view, name='customer_notifications'),

]
