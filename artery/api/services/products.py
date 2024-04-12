from ..models import Company, Product


def get_by_company(company_id: int):
    company = Company.objects.get(id=company_id)
    products = Product.objects.filter(company=company)
    return [
        {
            #'image': product.image,
            'name': product.name,
            'cost': product.cost,
            'size': product.size,
            'weight': product.weight,
            'description': product.description,
        }
        for product in products
    ]


def add_to_company(company_id: int, name: str, cost: float, size: float, weight: float, description: str):
    company = Company.objects.get(id=company_id)
    Product(
        company=company,
        name=name,
        cost=cost,
        size=size,
        weight=weight,
        description=description
    ).save()