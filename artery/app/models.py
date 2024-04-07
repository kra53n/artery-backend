from django.db import models


class Company(models.Model):
    ''' Role '''
    image = models.BinaryField(blank=True)
    name = models.CharField(max_length=32)
    email = models.EmailField()
    password = models.CharField(max_length=64)
    phone = models.CharField(max_length=11)
    description = models.TextField(blank=True)


class Client(models.Model):
    ''' Role '''
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


class City(models.Model):
    ''' Map element '''
    name = models.CharField(max_length=32)
    location_x = models.FloatField()
    location_y = models.FloatField()


class Stock(models.Model):
    ''' Map element '''
    name = models.CharField(max_length=32)
    city_id = models.ForeignKey(
        'City',
        on_delete=models.CASCADE
    ) 


class Transit(models.Model):
    ''' Map element '''
    city_id = models.ForeignKey(
        'City',
        on_delete=models.CASCADE
    )


class PickPoint(models.Model):
    ''' Map element '''
    name = models.CharField(max_length=32)
    city_id = models.ForeignKey(
        'City',
        on_delete=models.CASCADE
    ) 
    

class Road(models.Model):
    ''' Map element '''
    city_id_a = models.ForeignKey(
        'City',
        related_name='city_road_id_a',
        on_delete=models.CASCADE
    )
    city_id_b = models.ForeignKey(
        'City',
        related_name='city_road_id_b',
        on_delete=models.CASCADE
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


class Product(models.Model):
    ''' Order element '''
    image = models.BinaryField(blank=True)
    name = models.CharField(max_length=32)
    cost = models.FloatField()
    size = models.FloatField()
    weight = models.FloatField()
    description = models.TextField(blank=True)


class Order(models.Model):
    ''' Order element '''
    city_id_a = models.ForeignKey(
        'City',
        related_name='city_order_id_a',
        on_delete=models.PROTECT
    )
    city_id_b = models.ForeignKey(
        'City',
        related_name='city_order_id_b',
        on_delete=models.PROTECT
    )
    

class OrderProduct(models.Model):
    ''' Intermediate model '''
    order_id = models.ForeignKey(
        'Order',
        on_delete=models.CASCADE
    )
    product_id = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE
    ) 
    

class CompanyProduct(models.Model):
    ''' Intermediate model '''
    company_id = models.ForeignKey(
        'Company',
        on_delete=models.CASCADE
    )
    product_id = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE
    )
    

class StockProduct(models.Model):
    ''' Intermediate model '''
    stock_id = models.ForeignKey(
        'Stock',
        on_delete=models.CASCADE
    )
    product_id = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE
    )
    amount = models.PositiveIntegerField()
