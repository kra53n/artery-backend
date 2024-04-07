from django.db import models

# Create your models here.

# Roles 
class Company(models.Model):
    image = models.BinaryField(blank=True)
    name = models.CharField(max_length=32)
    email = models.EmailField()
    password = models.CharField(max_length=64)
    phone = models.CharField(max_length=11)
    description = models.TextField(blank=True)

class Client(models.Model):
    surname = models.CharField(max_length=32)
    name = models.CharField(max_length=32)
    patronymic = models.CharField(max_length=32, blank=True)
    phone = models.CharField(max_length=11)
    email = models.EmailField()
    password = models.CharField(max_length=64)
    image = models.BinaryField(blank=True)
    city_id = models.ForeignKey(
        'City',
        on_delete=models.PROTECT
    )


# Map elements
class City(models.Model):
    name = models.CharField(max_length=32)
    location_x = models.FloatField()
    location_y = models.FloatField()

class Stock(models.Model):
    name = models.CharField(max_length=32)
    city_id = models.ForeignKey(
        'City',
        on_delete=models.CASCADE
    ) 

class Transit(models.Model):
    city_id = models.ForeignKey(
        'City',
        on_delete=models.CASCADE
    )

class PickPoint(models.Model):
    name = models.CharField(max_length=32)
    city_id = models.ForeignKey(
        'City',
        on_delete=models.CASCADE
    ) 
    
class Road(models.Model):
    city_id_a = models.foreignkey(
        'City',
        on_delete=models.cascade
    )
    city_id_b = models.foreignkey(
        'City',
        on_delete=models.cascade
    )
    lenth = models.FloatField()
    time = models.TimeField()
    cost = models.FloatField()
    TRANSPORT_TYPE = {
        'CAR': 'car',
        'RAILWAY': 'railway',
        'AIR': 'air',
        'SEA': 'sea',
        'RIVER': 'river'
    }
    transport_type = models.CharField(max_length=7, choices=TRANSPORT_TYPE)


# Order
class Product(models.Model):
    image = models.BinaryField(blank=True)
    name = models.CharField(max_length=32)
    cost = models.FloatField()
    size = models.FloatField()
    weight = models.FloatField()
    description = models.TextField(black=True)

class Order(models.Model):
    city_id_a = models.ForeignKey(
        'City',
        on_delete=models.PROTECT
    )
    city_id_b = models.ForeignKey(
        'City',
        on_delete=models.PROTECT
    )
    

# Intermediate tables
class OrderProduct(models.Model):
    order_id = models.ForeignKey(
        'Order',
        on_delete=models.CASCADE
    )
    product_id = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE
    ) 
    
class CompanyProduct(models.Model):
    company_id = models.ForeignKey(
        'Company',
        on_delete=models.CASCADE
    )
    product_id = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE
    )
    
class StockProduct(models.Model):
    stock_id = models.ForeignKey(
        'Stock',
        on_delete=models.CASCADE
    )
    product_id = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE
    )
    amount = models.PositiveIntegerField()