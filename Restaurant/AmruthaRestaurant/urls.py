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
]
