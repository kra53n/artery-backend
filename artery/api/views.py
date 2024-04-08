from django.shortcuts import render
from django.http import HttpResponse
from django.views import View

from .models import City, Client


def index(request):
    return HttpResponse('u r at the index page of the api')


class RegisterClient(View):
    def get(self, request):
        return HttpResponse('wait the post query')

    def post(self, request):
        self._request = request
        if self._has_empty_required_fields:
            return HttpResponse(f'unfilled next required fields: {empty_required_fields}')
        valid, err = self._fields_are_valid()
        if not valid:
            return HttpResponse('unvalid fields')
        self._save_client()
        return HttpResponse(f'client was saved: {self._c}')

    @property
    def _has_empty_required_fields(self) -> bool:
        return len([f for f in Client.required_fields if f not in self._request.POST]) > 0

    @property
    def _fields_from_post(self) -> dict:
        fields_from_post = {f: self._request.POST[f] for f in Client.all_fields if f in self._request.POST}
        fields_from_post['city_id'] = City.objects.get(id=fields_from_post['city_id'])
        return fields_from_post
        
    def _fields_are_valid(self) -> (bool, str):
        return True, ''

    def _save_client(self):
        self._c = Client(**self._fields_from_post)
        self._c.save()


def register_company(request):
    return HttpResponse('u r at the client registration page')


def login_client(request):
    return HttpResponse('u r at the client logining page')


def login_company(request):
    return HttpResponse('u r at the company logining page')
