from ..models import Company


def get_info_by_company(company_id: int) -> dict:
    company = Company.objects.get(id=company_id)
    return {
        #'image': company.image,
        'name': company.name,
        'email': company.email,
        'phone': company.phone,
        'description': company.description,
    }


def get_all() -> list[dict]:
    return [
        {
            'company_id': company.id
        }
        for company in Company.objects.all()
    ]