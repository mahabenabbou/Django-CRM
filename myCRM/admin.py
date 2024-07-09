from django.contrib import admin

from .models import Customer,Order,Product,OrderItem,Shipment,Task,ContactLog

# Register your models here.

admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(Product)
admin.site.register(OrderItem)
admin.site.register(Shipment)
admin.site.register(Task)
admin.site.register(ContactLog)
