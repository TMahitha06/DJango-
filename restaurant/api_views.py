from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q, Count, Sum, Avg, Min, Max, F
from decimal import Decimal
from django.http import HttpResponse
from .models import MenuItem, Customers, Staff, Table, Order, OrderItem, Reservation
from .serializers import (
    MenuItemSerializer, CustomerSerializer, StaffSerializer,
    TableSerializer, OrderSerializer, OrderItemSerializer, ReservationSerializer
)


class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    @action(detail=False, methods=['get'], url_path='or-query')
    def or_query(self, request):
        items = MenuItem.objects.filter(Q(category='Appetizer') | Q(price__lt=100))
        serializer = self.get_serializer(items, many=True)
        return Response({"query": "Appetizers OR under RS100", "count": items.count(), "results": serializer.data})

    @action(detail=False, methods=['get'], url_path='and-query')
    def and_query(self, request):
        items = MenuItem.objects.filter(Q(category='Appetizer') & Q(price__gt=200))
        serializer = self.get_serializer(items, many=True)
        return Response({"query": "Appetizers AND over RS200", "count": items.count(), "results": serializer.data})

    @action(detail=False, methods=['get'], url_path='not-query')
    def not_query(self, request):
        items = MenuItem.objects.filter(~Q(category='Beverage'))
        serializer = self.get_serializer(items, many=True)
        return Response({"query": "All except beverages", "count": items.count(), "results": serializer.data})

    @action(detail=False, methods=['get'], url_path='complex-query')
    def complex_query(self, request):
        items = MenuItem.objects.filter(
            (Q(category='Appetizer') & Q(price__gt=250)) | (Q(category='Main Course') & Q(price__lt=200)))
        serializer = self.get_serializer(items, many=True)
        return Response({"query": "Complex Query", "count": items.count(), "results": serializer.data})

    @action(detail=False, methods=['get'], url_path='with-tax')
    def with_tax(self, request):
        items = MenuItem.objects.annotate(price_with_tax=F('price') * Decimal('1.18'))
        serializer = self.get_serializer(items, many=True)
        return Response({"message": "Items with 18% tax", "count": items.count(), "results": serializer.data})

    @action(detail=False, methods=['get'], url_path='stats')
    def stats(self, request):
        stats = MenuItem.objects.aggregate(
            total_items=Count('item_id'),
            average_price=Avg('price'),
            cheapest=Min('price'),
            most_expensive=Max('price'),
            total_value=Sum('price')
        )
        return Response({k: float(v) if v else 0 for k, v in stats.items()})


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customers.objects.all()
    serializer_class = CustomerSerializer

    @action(detail=False, methods=['get'], url_path='with-spending')
    def with_spending(self, request):
        customers = Customers.objects.annotate(
            total_spent=Sum('order__total_amount'),
            order_count=Count('order')
        ).filter(total_spent__isnull=False).order_by('-total_spent')
        serializer = self.get_serializer(customers, many=True)
        return Response({"message": "Customers by spending", "count": customers.count(), "results": serializer.data})


class StaffViewSet(viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer


class TableViewSet(viewsets.ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @action(detail=False, methods=['get'], url_path='stats')
    def stats(self, request):
        stats = Order.objects.aggregate(
            total_orders=Count('order_id'),
            total_revenue=Sum('total_amount'),
            average_order=Avg('total_amount'),
            highest_order=Max('total_amount')
        )
        return Response({k: float(v) if v else 0 for k, v in stats.items()})

    @action(detail=False, methods=['get'], url_path='by-status')
    def by_status(self, request):
        status_stats = Order.objects.values('order_status').annotate(
            count=Count('order_id'),
            total_revenue=Sum('total_amount')
        )
        return Response(status_stats)


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer


def api_links_page(request):
    """Simple page showing all API endpoints"""
    links = [
        ("/api/menu-items/", "Menu Items"),
        ("/api/customers/", "Customers"),
        ("/api/staff/", "Staff"),
        ("/api/tables/", "Tables"),
        ("/api/orders/", "Orders"),
        ("/api/order-items/", "Order Items"),
        ("/api/reservations/", "Reservations"),
        ("/api/menu-items/or-query/", "OR Query - Appetizers OR under RS100"),
        ("/api/menu-items/and-query/", "AND Query - Appetizers AND over RS200"),
        ("/api/menu-items/not-query/", "NOT Query - All except beverages"),
        ("/api/menu-items/complex-query/", "Complex Query"),
        ("/api/menu-items/with-tax/", "Items with 18% Tax"),
        ("/api/menu-items/stats/", "Menu Statistics"),
        ("/api/customers/with-spending/", "Customer Spending"),
        ("/api/orders/stats/", "Order Statistics"),
        ("/api/orders/by-status/", " Orders by Status"),
    ]

    html = """
    <html>
    <head>
        <title>Restaurant API</title>
        <style>
            body{font-family:Arial;max-width:900px;margin:50px auto;padding:20px}
            li{margin:15px 0}
            a{color:deepblue;text-decoration:none;font-size:14px}
            a:hover{text-decoration:underline}
            code{color:#666;font-size:14px}
            h1{color:#2c3e50}
        </style>
    </head>
    <body>
        <h1>Restaurant API - All Endpoints</h1>
        <ul>
    """
    for url, name in links:
        html += f'<li><a href="{url}">{name}</a><br><code>{url}</code></li>'
    html += "</ul></body></html>"
    return HttpResponse(html)