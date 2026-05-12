from django.db import models
from django.utils import timezone


class menuitem(models.Model):
    item_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    cat = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} - {self.price}"

    class Meta:
        db_table = 'menu_items'

class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name()


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    table_num = models.IntegerField()
    staff_name = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, default='pending')

    def __str__(self):
        if self.customer:
            return f"Order {self.id} - {self.customer.full_name()}"
        return f"Order {self.id} - walkin"


# need to add this still - rushing
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=255)
    qty = models.IntegerField()  # short name
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)

    def subtotal(self):
        return self.qty * self.unit_price

class Reservation(models.Model):
    cust_name = models.CharField(max_length=200)
    date = models.DateField()
    guests = models.IntegerField()
    table_id = models.IntegerField()
    special_request = models.TextField(blank=True, null=True)