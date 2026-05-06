from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import (
    MenuItemViewSet, CustomerViewSet, StaffViewSet,
    TableViewSet, OrderViewSet, OrderItemViewSet, ReservationViewSet
)

router = DefaultRouter()
router.register(r'menu-items', MenuItemViewSet, basename='menu-items')
router.register(r'customers', CustomerViewSet, basename='customers')
router.register(r'staff', StaffViewSet, basename='staff')
router.register(r'tables', TableViewSet, basename='tables')
router.register(r'orders', OrderViewSet, basename='orders')
router.register(r'order-items', OrderItemViewSet, basename='order-items')
router.register(r'reservations', ReservationViewSet, basename='reservations')

urlpatterns = [
    path('', include(router.urls)),
]