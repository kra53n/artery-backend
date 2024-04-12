from .graph import make_route
from .roads import get_as_dict as get_as_dict_roads

from ..models import Client, Order, Order_Product, Company_City, City, Product, Road


def get_by_client(client_id: int):
    client = Client.objects.get(id=client_id)
    orders = Order.objects.filter(client=client)
    return [
        {
            'image': order.image,
            'city_start_id': order.city_start.id,
            'city_end_id': order.city_end.id,
            'status': order.status,
            'client_id': order.client.id,
            'product_id': Order_Product.objects.get(id=order).product.id,
        }
        for order in orders
    ]

    
def take_order(client_id: int, city_start_id: int, product_id: int):
    client = Client.objects.get(id=client_id)
    city_start = City.objects.get(id=city_start_id)
    city_end = City.objects.get(id=client.city.id)
    product = Product.objects.get(id=product_id)
    order = Order(
        city_start=city_start,
        city_end=city_end,
        status='PROCESS',
        client=client
   )
    order.save()
    Order_Product(
        order=order,
        product=product,
        # TODO: add amount processing in future
        amount=0,
    ).save()


# TODO: add by param in futer
# `by` can be 'length', 'cost', etc
def give_route(client_id: int, product_id: int, by: str):
    client = Client.objects.get(id=client_id)
    product = Product.objects.get(id=product_id)
    company = product.company
    company_cities = Company_City.objects.filter(company=company)

    roads = [get_as_dict_roads(r) for r in Road.objects.filter(company=company)]
    cities = [cc.id for cc in company_cities]
    storage_cities = [cc.id for cc in company_cities if cc.is_storage]
    client_city = client.city.id
    return make_route(cities, roads, storage_cities, client_city, by)
