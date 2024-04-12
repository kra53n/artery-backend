from ..models import Client, Order, Order_Product, City


def get_by_client(client_id: int):
    client = Client.objects.get(id=client_id)
    orders = Order.objects.filter(client=client)
    return [
        {
            'city_start_id': order.city_start.id,
            'city_end_id': order.city_end.id,
            'status': order.status,
            'client_id': order.client.id,
        }
        for order in orders
    ]

    
def take_order(client_id: int, city_start_id: int, product_id: int):
    client = Client.objects.get(id=client_id)
    city_start = City.objects.get(id=city_start_id)
    city_end = City.objects.get(id=client.city.id)
    product = Product.objcets.get(id=product_id)
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
