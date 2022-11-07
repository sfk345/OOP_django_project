from django.urls import path
from django.contrib.auth import views as auth_views


from design import views
from design.views import *

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),

    path('', Home.as_view(), name='home'),

    path('create_order/', create_order, name='create_order'),
    path('orders/', OrdersByUser.as_view(), name='orders'),
    path('delete_order/<pk>', DeleteOrder.as_view(), name='delete_order')
]
