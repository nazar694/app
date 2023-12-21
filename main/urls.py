from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('user/<str:username>/', views.user_page, name='user_page'),
    path('user/<str:username>/logout', views.logout, name='logout'),
    path('send_message/', views.send_message, name='send_message'),
]
