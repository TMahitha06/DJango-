from rest_framework import serializers
from .models import MenuItem, Customers, Staff, Table, Order, OrderItem, Reservation

class MenuItemSerializer(serializers.ModelSerializer):
    price_with_tax = serializers.SerializerMethodField()

    class Meta:
        model = MenuItem
        fields = ['item_id', 'item_name', 'price', 'category', 'price_with_tax']

    def get_price_with_tax(self, obj):
        from decimal import Decimal
        return float(obj.price * Decimal('1.18'))

class CustomerSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()
    total_spent = serializers.SerializerMethodField()
    order_count = serializers.SerializerMethodField()

    class Meta:
        model = Customers
        fields = ['customer_id', 'first_name', 'last_name', 'full_name', 'phone', 'email', 'total_spent', 'order_count']

    def get_total_spent(self, obj):
        from django.db.models import Sum
        total = obj.order_set.aggregate(total=Sum('total_amount'))['total']
        return total or 0

    def get_order_count(self, obj):
        return obj.order_set.count()

class StaffSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()

    class Meta:
        model = Staff
        fields = ['staff_id', 'first_name', 'last_name', 'full_name', 'role']


class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ['table_id', 'table_number', 'capacity']


class OrderSerializer(serializers.ModelSerializer):
    customer_name = serializers.ReadOnlyField(source='customer.full_name')
    staff_name = serializers.ReadOnlyField(source='staff.full_name')
    table_number = serializers.ReadOnlyField(source='table.table_number')

    class Meta:
        model = Order
        fields = ['order_id', 'customer', 'customer_name', 'table', 'table_number',
                  'staff', 'staff_name', 'order_date', 'total_amount', 'order_status']


class OrderItemSerializer(serializers.ModelSerializer):
    item_name = serializers.ReadOnlyField(source='menu_item.item_name')
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ['order_item_id', 'order', 'menu_item', 'item_name', 'quantity', 'price', 'subtotal']

    def get_subtotal(self, obj):
        return obj.quantity * obj.price

class ReservationSerializer(serializers.ModelSerializer):
    customer_name = serializers.ReadOnlyField(source='customer.full_name')
    table_number = serializers.ReadOnlyField(source='table.table_number')

    class Meta:
        model = Reservation
        fields = ['reservation_id', 'customer', 'customer_name', 'table', 'table_number',
                  'reservation_date', 'guests']