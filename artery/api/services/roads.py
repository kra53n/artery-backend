from ..models import Company, City, Road


def get_as_dict(road: Road):
    return {
        'city_start_id': road.city_start.id,
        'city_end_id': road.city_end.id,
        'length': road.length,
        'time': road.time,
        'cost': road.cost,
        'transport_type': road.transport_type,
    }


def get_by_company(company_id: int):
    roads = Road.objects.filter(company=Company.objects.get(id=company_id))
    return [get_as_dict(road) for road in roads]


def add_for_company(
    company_id: int,
    city_start_id: int,
    city_end_id: int,
    transport_type: str,
    length: float,
    time,
    cost: float,
):
    company = Company.objects.get(id=company_id)
    city_start = City.objects.get(id=city_start_id)
    city_end = City.objects.get(id=city_end_id)
    roads = Road.objects.filter(company=company, city_start=city_start, city_end=city_end)
    if roads:
        # TODO: add raising exception
        return
    if transport_type.upper() not in Road.TRANSPORT_TYPE:
        # TODO: add raising exception
        return
    Road(
        company=company,
        city_start=city_start,
        city_end=city_end,
        transport_type=transport_type,
        length=length,
        time=time,
        cost=cost,      
    ).save()


def delete(road_id: int):
    Road.objects.get(id=road_id).delete()


def edit(road_id: int, param: str, param_val):
    road = Road.objects.get(id=road_id)
    exec(f'road.{param} = {param_val}')
    road.save()