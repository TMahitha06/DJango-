
from django.contrib import admin
from .models import MenuItem, Customers, Staff, Table, Order, OrderItem, Reservation

admin.site.register(MenuItem)
admin.site.register(Customers)
admin.site.register(Staff)
admin.site.register(Table)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Reservation)