from ..models import Company, Product


def _get_dict(product: Product):
    return {
        'image': product.image,
        'name': product.name,
        'cost': product.cost,
        'size': product.size,
        'weight': product.weight,
        'description': product.description,
    }


def get(product_id: int):
    product = Product.objects.get(id=product_id)
    return _get_dict(product)


def get_all():
    products = Product.objects.all()
    return [_get_dict(product) for product in products]


def get_by_company(company_id: int):
    company = Company.objects.get(id=company_id)
    products = Product.objects.filter(company=company)
    return [_get_dict(product) for product in products]


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


def delete(product_id: int):
    Product.objects.get(id=product_id).delete()


def edit(product_id: int, param: str, param_val):
    product = Product.objects.get(id=product_id)
    exec(f'product.{param} = {param_val}')
    product.save()
