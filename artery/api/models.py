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


class Client(models.Model):
    ''' Role '''
    surname = models.CharField(max_length=32)
    name = models.CharField(max_length=32)
    patronymic = models.CharField(max_length=32, blank=True)
    phone = models.CharField(max_length=11, validators=[validate_phone])
    email = models.EmailField(validators=[EmailValidator])
    password = models.CharField(max_length=64, validators=[validate_password])
    image = models.BinaryField(blank=True)
    city = models.ForeignKey(
        'City',
        on_delete=models.PROTECT
    )

    required_fields = 'surname', 'name', 'phone', 'email', 'password', 'city'
    all_fields = 'surname', 'name', 'patronymic', 'phone', 'email', 'password', 'image', 'city'

    def get_dict(self):
        return {
            'who': 'client',
            'surname': self.surname,
            'name': self.name,
            'patronymic': self.patronymic,
            'phone': self.phone,
            'email': self.email,
            'password': self.password,
            'city': self.city.id,
        }

        def __str__(self):
            return f''


class City(models.Model):
    ''' Map element '''
    name = models.CharField(max_length=32, unique=True)
    location_x = models.FloatField()
    location_y = models.FloatField()

    def __str__(self):
        return f'{self.name} ({self.location_x}, {self.location_y})'


class Road(models.Model):
    ''' Map element '''
    company = models.ForeignKey(
        'Company',
        on_delete=models.CASCADE,
    )
    city_start = models.ForeignKey(
        'City',
        related_name='city_road_start',
        on_delete=models.CASCADE
    )
    city_end = models.ForeignKey(
        'City',
        related_name='city_road_end',
        on_delete=models.CASCADE
    )
    length = models.FloatField()
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
    company = models.ForeignKey(
        'Company',
        on_delete=models.CASCADE,
    )


class Order(models.Model):
    ''' Order element '''
    city_start = models.ForeignKey(
        'City',
        related_name='city_order_start',
        on_delete=models.PROTECT
    )
    city_end = models.ForeignKey(
        'City',
        related_name='city_order_end',
        on_delete=models.PROTECT
    )
    STATUSES = {
        'PROCESS': 'in processsing',
        'PAYED': 'was payed',
        'WENT': 'went',
        'ARRIVED': 'arrived',
        'CLOSED': 'closed',
        'CANCELED': 'canceled',
    }
    statuses = models.CharField(max_length=8, choices=STATUSES)
    

class Order_Product(models.Model):
    ''' Intermediate model '''
    order = models.ForeignKey(
        'Order',
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE
    ) 
    amount = models.IntegerField()


class Company_City(models.Model):
    ''' Intermediate model'''
    company = models.ForeignKey(
        'Company',
        on_delete=models.CASCADE,
    )
    city = models.ForeignKey(
        'City',
        on_delete=models.CASCADE,
    )
    is_storage = models.BooleanField()

    def __str__(self):
        return f'Company_City(id: {self.id}, company: {self.company}, city: {self.city})'


class Company_City_Product(models.Model):
    ''' Intermediate model '''
    company_city = models.ForeignKey(
        'Company_City',
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
    )
    amount = models.IntegerField()