import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restaurant_project.settings')
django.setup()

from restaurant.models import *
from django.db.models import Q, Count, Sum, Avg, Min, Max, F, ExpressionWrapper, FloatField
# ============================================================
# TASK 1: BULK CREATE
# ============================================================
print("\n" + "="*60)
print("TASK 1: BULK CREATE")
print("="*60)

new_items = [
    MenuItem(item_name="Tandoori Chicken", price=300, category="Appetizer"),
    MenuItem(item_name="Fish Curry", price=450, category="Main Course"),
    MenuItem(item_name="Fresh Lime Soda", price=70, category="Beverage"),
    MenuItem(item_name="Caramel Custard", price=120, category="Dessert"),
]
print("\nAdding 4 new items:")
for item in new_items:
    print(f"  - {item.item_name} (RS{item.price})")

MenuItem.objects.bulk_create(new_items)
print(f"\n Added 4 new items! Total: {MenuItem.objects.count()}")
# ============================================================
# TASK 2: Q OBJECTS
# ============================================================
print("\n" + "="*60)
print("TASK 2: Q OBJECTS")
print("="*60)

r1 = MenuItem.objects.filter(Q(category='Appetizer') | Q(price__lt=100))
print(f"\n1. OR (Appetizers OR under RS100): {r1.count()} items")

r2 = MenuItem.objects.filter(Q(category='Appetizer') & Q(price__gt=200))
print(f"2. AND (Appetizers AND over RS200): {r2.count()} items")

r3 = MenuItem.objects.filter(~Q(category='Beverage'))
print(f"3. NOT (All except beverages): {r3.count()} items")

r4 = MenuItem.objects.filter(
    (Q(category='Appetizer') & Q(price__gt=250)) |
    (Q(category='Main Course') & Q(price__lt=200))
)
print(f"4. Complex: {r4.count()} items")

# ============================================================
# TASK 3: ANNOTATIONS
# ============================================================
print("\n" + "="*60)
print("TASK 3: ANNOTATIONS")
print("="*60)
print("\n1. Adding 18% tax to menu items")
items = MenuItem.objects.annotate(
    price_with_tax=ExpressionWrapper(
        F('price') * 1.18,
        output_field=FloatField()
    )
)[:5]

for i in items:
    print(f"   {i.item_name}: RS{i.price:.2f} → RS{i.price_with_tax:.2f}")

# 2. Count orders per customer
print("\n2. Number of orders per customer")
cust = Customers.objects.annotate(
    order_count=Count('order')
).filter(order_count__gt=0)[:5]

for c in cust:
    print(f"   {c.full_name}: {c.order_count} orders")

# 3. Total spending per customer
print("\n3. Total spending per customer")
cust2 = Customers.objects.annotate(
    total_spent=Sum('order__total_amount')
).filter(total_spent__isnull=False)[:5]

for c in cust2:
    print(f"   {c.full_name}: RS{c.total_spent:.2f}")

# ============================================================
# TASK 4: AGGREGATIONS
# ============================================================
print("\n" + "="*60)
print("TASK 4: AGGREGATIONS")
print("="*60)

# 1. Menu statistics
stats = MenuItem.objects.aggregate(
    total=Count('item_id'),
    avg=Avg('price'),
    cheap=Min('price'),
    expensive=Max('price')
)
print(f"\n1. Menu Stats: {stats['total']} items, Avg RS{stats['avg']:.2f}")
print(f"   Cheapest: RS{stats['cheap']:.2f}, Most Expensive: RS{stats['expensive']:.2f}")

# 2. Category statistics
cat = MenuItem.objects.values('category').annotate(
    cnt=Count('item_id'),
    avg=Avg('price')
)
print("\n2. By Category:")
for c in cat:
    print(f"   {c['category']}: {c['cnt']} items, RS{c['avg']:.2f}")

# 3. Order statistics
orders = Order.objects.aggregate(
    total=Count('order_id'),
    revenue=Sum('total_amount')
)
print(f"\n3. Order Stats: {orders['total']} orders, RS{orders['revenue'] or 0:.2f} revenue")

