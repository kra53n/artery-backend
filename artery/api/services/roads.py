from ..models import Company, Road


def get_by_company(company_id: int):
    roads = Road.objects.filter(company=Company.objects.get(id=company_id))
    return [
        {
            'city_start_id': road.city_start.id,
            'city_end_id': road.city_end.id,
            'length': road.lenth,
            'time': road.time,
            'cost': road.cost,
            'transport_type': road.transport_type,
        }
        for road in roads
    ]