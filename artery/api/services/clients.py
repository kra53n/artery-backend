from ..models import City, Client, Company, Road


def change_city(client_id: int, city_id: int):
    city = City.objects.get(id=city_id)
    client = Client.objects.get(id=client_id)
    client.city = city
    client.save()


def get_available_cityies_in_company(company_id: int) -> list[int]:
    company = Company.objects.get(id=company_id)
    roads = Road.objects.filter(company=company)
    res = []
    for road in roads:
        res.append(road.city_start.id)
        res.append(road.city_end.id)
    return list(set(res))