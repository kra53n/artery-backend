from django.test import Client, TestCase

from .models import City


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
