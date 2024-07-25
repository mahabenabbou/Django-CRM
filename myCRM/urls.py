from django.urls import path
from . import views



urlpatterns = [
    path('', views.home , name='home'),
    path('logout/', views.logout_user , name='logout'),
    path('register/', views.register_user , name='register'),
    
    
    path('customers/', views.customers, name='customers'),

    path('orderitems/', views.orderitems, name='orderitems'),
    
    
    path('orders/', views.orders , name='orders'),
    path('moreinfoOrder/<int:pk>', views.moreinfoOrder , name='moreinfoOrder'),
    path('deleteOrder/<int:pk>', views.deleteOrder , name='deleteOrder'),
    path('updateOrder/<int:pk>', views.updateOrder , name='updateOrder'),
    path('addOrder/', views.addOrder , name='addOrder'),

    
    path('products/', views.products , name='products'),
    path('moreinfoProduct/<int:pk>', views.moreinfoProduct , name='moreinfoProduct'),
    path('deleteProduct/<int:pk>', views.deleteProduct , name='deleteProduct'),
    path('updateProduct/<int:pk>', views.updateProduct , name='updateProduct'),
    path('addProduct/', views.addProduct , name='addProduct'),

    
    path('shipments/', views.shipments , name='shipments'),
    path('moreinfoShipment/<int:pk>', views.moreinfoShipment , name='moreinfoShipment'),
    path('deleteShipment/<int:pk>', views.deleteShipment , name='deleteShipment'),
    path('updateShipment/<int:pk>', views.updateShipment , name='updateShipment'),
    path('addShipment/', views.addShipment , name='addShipment'),

    
    path('tasks/', views.tasks , name='tasks'),
    path('moreinfoTask/<int:pk>', views.moreinfoTask , name='moreinfoTask'),
    path('deleteTask/<int:pk>', views.deleteTask , name='deleteTask'),
    path('updateTask/<int:pk>', views.updateTask , name='updateTask'),
    path('addTask/', views.addTask , name='addTask'),
    
    
    path('contactlogs/', views.contactlogs , name='contactlogs'),
    path('moreinfoContactLog/<int:pk>', views.moreinfoContactLog , name='moreinfoContactLog'),
    path('deleteContactLog/<int:pk>', views.deleteContactLog , name='deleteContactLog'),
    path('updateContactLog/<int:pk>', views.updateContactLog , name='updateContactLog'),
    path('addContactLog/', views.addContactLog , name='addContactLog'),

     path('orders_per_month/', views.orders_per_month_view, name='orders_per_month_view')
]
