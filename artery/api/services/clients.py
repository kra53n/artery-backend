from ..models import City, Client


def change_city(client_id: int, city_id: int):
    city = City.objects.get(id=city_id)
    client = Client.objects.get(id=client_id)
    client.city = city
    client.save()