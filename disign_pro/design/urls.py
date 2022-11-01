from django.urls import path
from django.contrib.auth import views as auth_views


from design import views
from design.views import *

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),

    path('', home, name='home'),

    path('application/', application, name='application'),
    path('orders/', OrdersByUser.as_view(), name='orders'),
]
