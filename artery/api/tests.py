from django.test import Client, TestCase

from .models import Company, City
from .models import Client as ClientModel


class TestClientRegistration(TestCase):
    def test_correct_info(self):
        City(id=1, name='Москва', location_x=0.1, location_y=0.3).save()
        c = Client()
        response = c.post(
            '/api/register/client/',
            {
                'surname': 'asdf',
                'name': 'asdf',
                'phone': '31113339955',
                'email': 'example@gmail.com',
                'password': 'smth',
                'city_id': 1,
            },
        )
        assert response.json()['ok'] == True

    def test_incorrect_phone_with_letters(self):
        City(id=1, name='Москва', location_x=0.1, location_y=0.3).save()

        c = Client()
        response = c.post(
            '/api/register/client/',
            {
                'surname': 'asdf',
                'name': 'asdf',
                'phone': 'sadfsadf',
                'email': 'example@gmail.com',
                'password': 'smth',
                'city_id': 1,
            },
        )
        json = response.json()
        assert json['ok'] == False and 'phone' in json['info']

    def test_incorrect_phone_with_digits(self):
        City(id=1, name='Москва', location_x=0.1, location_y=0.3).save()

        c = Client()
        response = c.post(
            '/api/register/client/',
            {
                'surname': 'asdf',
                'name': 'asdf',
                'phone': '1231233',
                'email': 'example@gmail.com',
                'password': 'smth',
                'city_id': 1,
            },
        )
        json = response.json()
        assert json['ok'] == False and 'phone' in json['info']

    def test_email_collision(self):
        City(id=1, name='Москва', location_x=0.1, location_y=0.3).save()
        ClientModel(
            id=1,
            surname='asdasd',
            name='asdasd',
            phone='75345234644',
            email='example@gmail.com',
            password='123',
            city_id=City.objects.get(id=1)
        ).save()

        c = Client()
        response = c.post(
            '/api/register/client/',
            {
                'surname': 'asdf',
                'name': 'asdf',
                'phone': '12312345124',
                'email': 'example@gmail.com',
                'password': 'smth',
                'city_id': 1,
            },
        )
        assert response.json()['ok'] == False



class TestCompanyRegistration(TestCase):
    def test_correct_info(self):
        c = Client()
        response = c.post(
            '/api/register/company/',
            {
                'name': 'ExampleCompany',
                'email': 'example@gmai.com',
                'password': 'asdasd',
                'phone': '31113339955',
                'description': 'asdfsdf',
            },
        )
        assert response.json()['ok'] == True

    def test_not_full_info(self):
        c = Client()
        response = c.post(
            '/api/register/company/',
            {
                'name': 'ExampleCompany',
                'email': 'example@gmai.com',
                'password': 'asdasd',
                'phone': '31113339955',
            },
        )
        assert response.json()['ok'] == True

    def test_incorrect_phone_with_letters(self):
        pass

    def test_incorrect_phone_with_digits(self):
        pass

    def test_incorrect_email(self):
        pass

    def test_email_collision(self):
        Company(
            id=1,
            name='asdasd',
            phone='75345234644',
            email='example@gmail.com',
            password='123',
        ).save()

        c = Client()
        response = c.post(
            '/api/register/company/',
            {
                'name': 'asdf',
                'phone': '12312345124',
                'email': 'example@gmail.com',
                'password': 'smth',
            },
        )
        assert response.json()['ok'] == False


class TestClientLogining(TestCase):
    def test_correct_info(self):
        City(id=1, name='Москва', location_x=0.1, location_y=0.3).save()
        client_model = ClientModel(
            id=1,
            surname='asdasd',
            name='asdasd',
            phone='75345234644',
            email='example@gmail.com',
            password='123',
            city_id=City.objects.get(id=1)
        )
        client_model.save()

        c = Client()
        response = c.post(
            '/api/login/client/',
            {
                'email': 'example@gmail.com',
                'password': '123',
            },
        )
        assert response.json()['ok'] == True
