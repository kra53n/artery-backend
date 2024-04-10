from ..models import Company, Company_City


def get_by_company(company_id: int):
    company = Company.objects.get(id=company_id)
    company_cities = Company_City.objects.filter(company_id=company)
    return [
        {
            'city_id': company_city.city.id,
            'name': company_city.city.name,
            'x': company_city.city.location_x,
            'y': company_city.city.location_y,
            'is_storage': company_city.is_storage,
        }
        for company_city in company_cities
    ]