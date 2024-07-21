
from django.urls import path
from . import views



urlpatterns = [
    path('', views.home , name='home'),
    path('logout/', views.logout_user , name='logout'),
    path('register/', views.register_user , name='register'),
    path('customers/', views.customers, name='customers'),
    path('orders/', views.orders , name='orders'),
    path('products/', views.products , name='products'),
    path('shipments/', views.shipments , name='shipments'),
    path('tasks/', views.tasks , name='tasks'),
    path('contactlogs/', views.contactlogs , name='contactlogs'),
    path('moreinfo/<int:pk>', views.moreinfo , name='moreinfo'),
    path('delete/<int:pk>', views.delete , name='delete'),
    path('update/<int:pk>', views.update , name='update'),
    path('add/', views.add , name='add'),
]
