from django.contrib import auth
from django.core.exceptions import ValidationError
from django.http import JsonResponse, HttpResponse
from django.views import View

from .services import cities
from .models import Company, City, Client


def index(request):
    return HttpResponse('u r at the index page of the api')


def logout(request):
    auth.logout(request)
    return JsonResponse({'ok': True})


class ViewWithGet(View):
    def get(self, request):
        return HttpResponse('wait the post request')


class Me(ViewWithGet):
    def post(self, request):
        if 'client_id' in request.session:
            return JsonResponse({
                'ok': True,
                'info': Client.objects.get(id=request.session['client_id']).get_dict(),
            })
        if 'company_id' in request.session:
            return JsonResponse({
                'ok': True,
                'info': Company.objects.get(id=request.session['company_id']).get_dict(),
            })
        return JsonResponse({'ok': False, 'info': 'the user is not logged in'})


class RegisterClient(ViewWithGet):
    def post(self, request):
        self._request = request
        empty_required_fields = [f for f in Client.required_fields if f not in self._request.POST]
        if empty_required_fields:
            return JsonResponse({'ok': False, 'info': ['unfilled required fields', empty_required_fields]})
        if self._email_already_exists:
            return JsonResponse({'ok': False, 'info': f'email({self._request.POST["email"]}) already exists'})
        self._c = Client(**self._fields_from_post)
        try:
            self._c.clean_fields()
        except ValidationError as e:
            return JsonResponse({'ok': False, 'info': e.message_dict})
        return JsonResponse({'ok': True})

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
            return JsonResponse({'ok': False, 'info': ['unfilled required fields', empty_required_fields]})
        if self._email_already_exists:
            return JsonResponse({'ok': False, 'info': f'email({self._request.POST["email"]}) already exists'})
        self._c = Company(**self._fields_from_post)
        try:
            self._c.clean_fields()
        except ValidationError as e:
            return JsonResponse({'ok': 'False', 'info': e.message_dict})
        return JsonResponse({'ok': True})

    @property
    def _email_already_exists(self) -> bool:
        return len(Company.objects.filter(email=self._request.POST['email'])) > 0

    @property
    def _fields_from_post(self) -> dict:
        fields_from_post = {f: self._request.POST[f] for f in Company.all_fields if f in self._request.POST}
        return fields_from_post


class LoginClient(ViewWithGet):
    def get(self, request):
        client = Client.objects.get(email='greasha46@gmail.com')
        request.session['client_id'] = client.id
        return HttpResponse('wait the post request')

    def post(self, request):
        self._request = request
        if self._missed_fields:
            return JsonResponse({'ok': False, 'info': ['missed fields', self._missed_fields]})
        email = request.POST['email']
        try:
            client = Client.objects.get(email=email)
        except Client.DoesNotExist:
            return JsonResponse({'ok': False, 'info': f'client with email({email}) does not exist'})
        if client.password != request.POST['password']:
            return JsonResponse({'ok': False, 'info': f'incorrect login for the email({email})'})
        request.session['client_id'] = client.id
        return JsonResponse({'ok': True})

    @property
    def _missed_fields(self) -> list['str']:
        fields = 'email', 'password'
        missed_fields = [f for f in fields if f not in self._request.POST]
        return missed_fields


class LoginCompany(ViewWithGet):
    def get(self, request):
        return HttpResponse('wait the post request')

    def post(self, request):
        self._request = request
        if self._missed_fields:
            return JsonResponse({'ok': False, 'info': ['missed fields', self._missed_fields]})
        email = request.POST['email']
        try:
            company = Company.objects.get(email=email)
        except Client.DoesNotExist:
            return JsonResponse({'ok': False, 'info': f'company with email({email}) does not exist'})
        if company.password != request.POST['password']:
            return JsonResponse({'ok': False, 'info': f'incorrect login for the email({email})'})
        request.session['company_id'] = company.id
        return JsonResponse({'ok': True})

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


class CompanyCities(ViewWithGet):
    '''
    Send the cities available for the company
    '''
    def get(self, request):
        if 'company_id' not in request.session or 'client_id' not in request.session:
            return JsonResponse({'ok': False, 'info': 'the user is not logged in'})
        if 'company_id' not in request.POST:
            return JsonResponse({'ok': False, 'info': 'company id was not given'})
        return JsonResponse({'ok': True, 'info': cities.get_by_company(request.POST['company_id'])})
