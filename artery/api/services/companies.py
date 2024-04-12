from ..models import Company


def get_all() -> list[dict]:
    return [
        {
            'company_id': company.id
        }
        for company in Company.objects.all()
    ]