from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views import View

from .models import City, Client


def index(request):
    return HttpResponse('u r at the index page of the api')


class RegisterClient(View):
    def get(self, request):
        return HttpResponse('wait the post request')

    def post(self, request):
        self._request = request
        empty_required_fields = [f for f in Client.required_fields if f not in self._request.POST]
        if len(empty_required_fields):
            return JsonResponse({'ok': False, 'info': ['unfilled required fields', empty_required_fields]})
        self._c = Client(**self._fields_from_post)
        try:
            self._c.clean_fields()
        except ValidationError as e:
            return JsonResponse({'ok': False, 'info': e.message_dict})
        return JsonResponse({'ok': True})

    @property
    def _fields_from_post(self) -> dict:
        fields_from_post = {f: self._request.POST[f] for f in Client.all_fields if f in self._request.POST}
        fields_from_post['city_id'] = City.objects.get(id=fields_from_post['city_id'])
        return fields_from_post


def register_company(request):
    return HttpResponse('u r at the client registration page')


def login_client(request):
    return HttpResponse('u r at the client logining page')


def login_company(request):
    return HttpResponse('u r at the company logining page')
