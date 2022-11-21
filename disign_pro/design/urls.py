from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth import views as auth_views


from design import views
from design.views import *

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),

    path('', Home.as_view(), name='home'),

    path('orders/delete', views.deletecategory, name='del_category'),
    path('orders/add', views.AddCategory.as_view(), name='add_category'),
    path('orders/', views.OrdersAdmin.as_view(), name='adm_orders'),
    path('orders/<int:pk>/change_of_status', views.changeofstatus, name='change_of_status'),
    path('orders/<int:pk>/full_status_change/', views.FullStatusChange.as_view(), name='full_status_change'),
    path('orders/<int:pk>/accepted_status_change/', views.AcceptedStatusChange.as_view(), name='accepted_status_change'),
    path('order/<pk>', views.DetailOrder.as_view(), name='detail_order'),

    path('create_order/', create_order, name='create_order'),
    path('myorders/', OrdersByUser.as_view(), name='myorders'),
    path('delete_order/<pk>', DeleteOrder.as_view(), name='delete_order')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
