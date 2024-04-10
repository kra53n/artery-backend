from ..models import Company, Road


def get_by_company(company_id: int):
    return Road.objects.filter(company=Company.objects.get(id=company_id))