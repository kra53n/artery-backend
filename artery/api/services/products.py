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