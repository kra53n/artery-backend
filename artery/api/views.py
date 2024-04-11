from django.contrib import auth
from django.core.exceptions import ValidationError
from django.http import JsonResponse, HttpResponse
from django.views import View

from .services import cities, roads
from .shortcuts import json_response
from .models import Company, Company_City, City, Client


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


class ProductAdd(ViewWithGet):
    pass


class ProductGet(ViewWithGet):
    pass


class OrderTake(ViewWithGet):
    pass


class OrderInfo(ViewWithGet):
    pass


class GetAllCities(ViewWithGet):
    def get(self, _):
        return json_response(ok=True, info=cities.get_all())


class CompanyCities(ViewWithGet):
    '''
    Send available cities for the company
    '''
    def _check_company_id(method):
        def wrapper(*args):
            company_id = None
            request = args[1]
            if 'company_id' in request.session:
                company_id = request.session['company_id']
            # TODO: delete this block of condition due unsecurity
            elif 'company_id' in request.POST:
                 company_id = request.POST['company_id']
            if company_id:
                return method(*args, company_id)
            return json_response(
                ok=False,
                info='company id was not given',
                status=400,
            )
        return wrapper

    _check_company_id = staticmethod(_check_company_id)

    @_check_company_id
    def post(self, _, company_id):
        return json_response(ok=True, info=cities.get_by_company(company_id))

class CompanyCitiesAdd(ViewWithGet):
    @CompanyCities._check_company_id
    def post(self, request, company_id):
        if 'city_id' in request.POST:
            is_storage = 'is_storage' in request.POST and request.POST['is_storage'].lower() == 'true'
            cities.add_for_company(request.POST['city_id'], company_id, is_storage)
            return json_response(True)
        return json_response(ok=False, info='city_id was not given')


class CompanyCitiesDel(ViewWithGet):
    @CompanyCities._check_company_id
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
    @CompanyCities._check_company_id
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
    def post(self, request):
        company_id = None
        if 'company_id' in request.session:
            company_id = request.session['company_id']
        elif 'company_id' in request.POST:
            company_id = request.POST['company_id']
        return json_response(
            ok=True,
            info=roads.get_by_company(company_id),
        ) if company_id else json_response(
            ok=False,
            info='company id was not given',
            status=400,
        )