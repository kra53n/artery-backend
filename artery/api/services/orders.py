from ..models import Client, Order


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