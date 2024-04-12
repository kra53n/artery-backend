from django.contrib import auth
from django.core.exceptions import ValidationError
from django.http import JsonResponse, HttpResponse
from django.views import View

from .services import cities, clients, orders, products, roads
from .shortcuts import json_response
from .models import Company, Company_City, City, Client
from .views_utils import check_fields, check_logged_in_under_company, check_logged_in_under_client


def index(request):
    return HttpResponse('u r at the index page of the api')


def logout(request):
    auth.logout(request)
    return json_response(True)


class ViewWithGet(View):
    def get(self, request):
        return HttpResponse('wait the post request')


class Me(ViewWithGet):
    def get(self, request):
        if 'client_id' in request.session:
            return json_response(
                ok=True,
                info=Client.objects.get(id=request.session['client_id']).get_dict(),
            )
        if 'company_id' in request.session:
            return json_response(
                ok=True,
                info=Company.objects.get(id=request.session['company_id']).get_dict(),
            )
        return json_response(ok=False, info='the user is not logged in', status=401)


class RegisterClient(ViewWithGet):
    def post(self, request):
        self._request = request
        empty_required_fields = [f for f in Client.required_fields if f not in self._request.POST]
        if empty_required_fields:
            return json_response(
                ok=False,
                info=['unfilled required fields', empty_required_fields],
                status=400,
            )
        if self._email_already_exists:
            return json_response(
                ok=False,
                info=f'email({self._request.POST["email"]}) already exists',
                status=400,
            )
        self._c = Client(**self._fields_from_post)
        try:
            self._c.clean_fields()
        except ValidationError as e:
            return json_response(ok=False, info=e.message_dict, status=400)
        except City.DoesNotExist:
            return json_response(
                ok=False,
                info='given city does not exist',
                status=400
            )
        self._c.save()
        return json_response(True)

    @property
    def _email_already_exists(self) -> bool:
        return len(Client.objects.filter(email=self._request.POST['email'])) > 0

    @property
    def _fields_from_post(self) -> dict:
        fields_from_post = {f: self._request.POST[f] for f in Client.all_fields if f in self._request.POST}
        fields_from_post['city'] = City.objects.get(id=fields_from_post['city'])
        return fields_from_post


class RegisterCompany(ViewWithGet):
    def post(self, request):
        self._request = request
        empty_required_fields = [f for f in Company.required_fields if f not in self._request.POST]
        if empty_required_fields:
            return json_response(
                ok=False,
                info=['unfilled required fields', empty_required_fields],
                status=400,
            )
        if self._email_already_exists:
            return json_response(
                ok=False,
                info=f'email({self._request.POST["email"]}) already exists',
                status=400,
            )
        self._c = Company(**self._fields_from_post)
        try:
            self._c.clean_fields()
        except ValidationError as e:
            return json_response(ok=False, info=e.message_dict, status=400)
        self._c.save()
        return json_response(True)

    @property
    def _email_already_exists(self) -> bool:
        return len(Company.objects.filter(email=self._request.POST['email'])) > 0

    @property
    def _fields_from_post(self) -> dict:
        fields_from_post = {f: self._request.POST[f] for f in Company.all_fields if f in self._request.POST}
        return fields_from_post



class LoginClient(ViewWithGet):
    def post(self, request):
        self._request = request
        if self._missed_fields:
            return json_response(
                ok=False,
                info=['missed fields', self._missed_fields],
                status=400,
            )
        email = request.POST['email']
        try:
            client = Client.objects.get(email=email)
        except Client.DoesNotExist:
            return json_response(
                ok=False,
                info=f'client with email({email}) does not exist',
                status=400,
            )
        if client.password != request.POST['password']:
            return json_response(
                ok=False,
                info=f'incorrect password for the email({email})',
                status=400,
            )
        request.session['client_id'] = client.id
        return json_response(True)

    @property
    def _missed_fields(self) -> list['str']:
        fields = 'email', 'password'
        missed_fields = [f for f in fields if f not in self._request.POST]
        return missed_fields


class LoginCompany(ViewWithGet):
    def post(self, request):
        self._request = request
        if self._missed_fields:
            return json_response(
                ok=False,
                info=['missed fields', self._missed_fields],
                status=400
            )
        email = request.POST['email']
        try:
            company = Company.objects.get(email=email)
        except Company.DoesNotExist:
            return json_response(
                ok=False,
                info=f'company with email({email}) does not exist',
                status=400,
            )
        if company.password != request.POST['password']:
            return json_response(
                ok=False,
                info=f'incorrect password for the email({email})',
                status=400,
            )
        request.session['company_id'] = company.id
        return json_response(True)

    @property
    def _missed_fields(self) -> list['str']:
        fields = 'email', 'password'
        missed_fields = [f for f in fields if f not in self._request.POST]
        return missed_fields


class GetAllCities(ViewWithGet):
    def get(self, _):
        return json_response(ok=True, info=cities.get_all())


class CompanyCities(ViewWithGet):
    '''
    Send available cities for the company
    '''
    @check_fields('company_id')
    def post(self, _, company_id):
        return json_response(ok=True, info=cities.get_by_company(company_id))


class CompanyCitiesAdd(ViewWithGet):
    @check_fields('company_id')
    def post(self, request, company_id):
        if 'city_id' in request.POST:
            is_storage = 'is_storage' in request.POST and request.POST['is_storage'].lower() == 'true'
            cities.add_for_company(request.POST['city_id'], company_id, is_storage)
            return json_response(True)
        return json_response(ok=False, info='city_id was not given')


class CompanyCitiesDel(ViewWithGet):
    @check_fields('company_id')
    def post(self, request, company_id):
        if 'city_id' in request.POST:
            city_id = request.POST['city_id']
            try:
                cities.del_in_company(city_id, company_id)
            except Company_City.DoesNotExist:
                return json_response(
                    ok=False,
                    info=f'impossible to delete city({city_id})',
                    status=400,
                )
            return json_response(True)
        return json_response(
            ok=False,
            info='city_id was not given',
            status=400
        )


class CompanyCitiesEdit(ViewWithGet):
    @check_fields('company_id')
    def post(self, request, company_id):
        if 'city_id' in request.POST:
            is_storage = 'is_storage' in request.POST and request.POST['is_storage'].lower() == 'true'
            city_id = request.POST['city_id']
            try:
                cities.edit_of_company(city_id, company_id, is_storage)
            except Company_City.DoesNotExist:
                return json_response(
                    ok=False,
                    info=f'impossible to edit city({city_id})',
                    status=400,
                )
            return json_response(True)
        return json_response(
            ok=False,
            info='city_id was not given',
            status=400
        )


class CompanyRoads(ViewWithGet):
    '''
    Send roads of the company
    '''
    @check_fields('company_id')
    def post(self, _, company_id):
        return json_response(
            ok=True,
            info=roads.get_by_company(company_id),
        )


class CompanyRoadsAdd(ViewWithGet):
    @check_fields(
        'company_id',
        'city_start_id',
        'city_end_id',
        'transport_type',
        'length',
        'time',
        'cost',
    )
    def post(
        self,
        _,
        company_id: int,
        city_start_id: int,
        city_end_id: int,
        transport_type,
        length: float,
        time,
        cost: float,
    ):
        # TODO: add exceptions for each incorrect field
        return json_response(
            ok=True,
            info=roads.add_for_company(
                company_id,
                city_start_id,
                city_end_id,
                transport_type,
                length,
                time,
                cost,
            )
        )


class CompanyRoadsDel(ViewWithGet):
    @check_logged_in_under_company
    @check_fields('road_id')
    def post(self, request, road_id: int):
        # TODO: add exceptions
        return json_response(
            ok=True,
            info=roads.delete(road_id),
        )


class CompanyRoadsEdit(ViewWithGet):
    '''
    This view possible to use in one way: change one parameter per request.
    '''
    @check_logged_in_under_company
    @check_fields('road_id', 'param', 'param_val')
    def post(self, request, road_id: int, param: str, param_val):
        # TODO: add exceptions
        return json_response(
            ok=True,
            info=roads.edit(road_id, param, param_val),
        )


class CompanyProducts(ViewWithGet):
    @check_fields('company_id')
    def post(self, _, company_id):
        # TODO: add exceptions
        return json_response(
            ok=True,
            info=products.get_by_company(company_id),
        )
    

class CompanyProductsAdd(ViewWithGet):
    @check_logged_in_under_company
    @check_fields(
        'company_id',
        'name',
        'cost',
        'size',
        'weight',
        'description'
    )
    def post(
        self,
        _,
        company_id: int,
        name: str,
        cost: float,
        size: float,
        weight: float,
        description: str
    ):
        # TODO: add exceptions
        return json_response(
            ok=True,
            info=products.add_to_company(
                company_id,
                name,
                cost,
                size,
                weight,
                description,
            )
        )

        
class CompanyProductsDel(ViewWithGet):
    @check_logged_in_under_company
    @check_fields('product_id')
    def post(self, _, product_id: int):
        # TODO: add exceptions
        return json_response(
            ok=True,
            info=products.delete(product_id)
        )
        

class CompanyProductsEdit(ViewWithGet):
    @check_logged_in_under_company
    @check_fields('product_id', 'param', 'param_val')
    def post(self, _, product_id: int, param: str, param_val):
        # TODO: add exeptions
        return json_response(
            ok=True,
            info=products.edit(product_id, param, param_val)
        )


class ClientChangeCity(ViewWithGet):
    @check_logged_in_under_client
    @check_fields('client_id', 'city_id')
    def post(self, _, client_id, city_id):
        # TODO: add exceptions
        return json_response(
            ok=True,
            info=clients.change_city(client_id, city_id)
        )


class ClientOrders(ViewWithGet):
    @check_logged_in_under_client
    @check_fields('client_id')
    def post(self, _, client_id):
        return json_response(
            ok=True,
            info=orders.get_by_client(client_id),
        )


class ClientOrdersOrder(ViewWithGet):
    #@check_logged_in_under_client
    @check_fields('client_id', 'city_start_id')
    def post(
        self,
        _,
        client_id: int,
        city_start_id: int,
    ):
        # TODO: add exceptions
        return json_response(
            ok=True,
            info=orders.take_order(
                client_id,
                city_start_id
            )
        )

    
class ClientOrdersMakeRoute(ViewWithGet):
    @check_logged_in_under_client
    @check_fields('client_id')
    def post(sefl, _, client_id):
        pass