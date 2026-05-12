from rest_framework import serializers
from .models import MenuItem, Customers, Staff, Table, Order, OrderItem, Reservation

TAX_RATE = 1.18
class MenuItemSerializer(serializers.ModelSerializer):
    price_with_tax = serializers.SerializerMethodField()

    class Meta:
        model = MenuItem
        fields = ['item_id', 'item_name', 'price', 'category', 'price_with_tax']

    def get_price_with_tax(self, obj):
        return float(obj.price) * TAX_RATE

class CustomerSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='full_name', read_only=True)

    class Meta:
        model = Customers
        fields = ['customer_id', 'first_name', 'last_name', 'full_name', 'phone', 'email']


class StaffSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()

    class Meta:
        model = Staff
        fields = '__all__'


class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source='menu_item.item_name', read_only=True)
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ['order_item_id', 'order', 'menu_item', 'item_name', 'quantity', 'price', 'subtotal']

    def get_subtotal(self, obj):
        return obj.quantity * obj.price


class OrderSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.full_name', read_only=True, default='Walk-in')
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['order_id', 'customer', 'customer_name', 'table', 'staff',
                  'order_date', 'total_amount', 'order_status', 'items']

    def create(self, validated_data):
        # auto set total to 0, let order items manage it
        return super().create(validated_data)


class ReservationSerializer(serializers.ModelSerializer):
    customer_name = serializers.ReadOnlyField(source='customer.full_name')
    table_number = serializers.ReadOnlyField(source='table.table_number')

    class Meta:
        model = Reservation
        fields = ['reservation_id', 'customer', 'customer_name', 'table',
                  'table_number', 'reservation_date', 'guests']
