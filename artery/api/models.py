from django.core.validators import EmailValidator
from django.db import models

from .validators import validate_password, validate_phone


class Company(models.Model):
    ''' Role '''
    image = models.BinaryField(blank=True)
    name = models.CharField(max_length=32)
    email = models.EmailField(validators=[EmailValidator])
    password = models.CharField(max_length=64, validators=[validate_password])
    phone = models.CharField(max_length=11, validators=[validate_phone])
    description = models.TextField(blank=True)

    required_fields = 'name', 'email', 'password', 'phone'
    all_fields = 'image', 'name', 'email', 'password', 'phone', 'description'

    def get_dict(self):
        return {
            'who': 'company',
            'name': self.name,
            'email': self.email,
            'password': self.password,
            'phone': self.phone,
            'description': self.description,
        }


# TODO: rename ForeignKey's

class Client(models.Model):
    ''' Role '''
    surname = models.CharField(max_length=32)
    name = models.CharField(max_length=32)
    patronymic = models.CharField(max_length=32, blank=True)
    phone = models.CharField(max_length=11, validators=[validate_phone])
    email = models.EmailField(validators=[EmailValidator])
    password = models.CharField(max_length=64, validators=[validate_password])
    image = models.BinaryField(blank=True)
    city_id = models.ForeignKey(
        'City',
        on_delete=models.PROTECT
    )

    required_fields = 'surname', 'name', 'phone', 'email', 'password', 'city_id'
    all_fields = 'surname', 'name', 'patronymic', 'phone', 'email', 'password', 'image', 'city_id'

    def get_dict(self):
        return {
            'who': 'client',
            'surname': self.surname,
            'name': self.name,
            'patronymic': self.patronymic,
            'phone': self.phone,
            'email': self.email,
            'password': self.password,
            'city_id': self.city_id.id,
        }


class City(models.Model):
    ''' Map element '''
    name = models.CharField(max_length=32)
    location_x = models.FloatField()
    location_y = models.FloatField()

    def __str__(self):
        return f'{self.name} ({self.location_x}, {self.location_y})'


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
