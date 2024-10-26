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
    path('adminsignin/', views.adminsignin, name='adminsignin'),
    path('admindashboard/', views.admindashboard, name='admindashboard'),
    path('customermenu/', views.customermenu, name='customermenu'),
    path('customer_list/', views.customer_list, name='customer_list'),  # URL for the customer list page
    path('menu_items/', views.menu_items, name='menu_items'),
    path('add_item/', views.add_item, name='add_item'),


]
