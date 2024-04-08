from django.test import Client, TestCase

from .models import City


class TestClientRegistration(TestCase):
    def test_correct_info(self):
        City(name='Москва', location_x=0.1, location_y=0.3).save()

        c = Client()
        response = c.post(
            '/api/register/client/',
            {
                'surname': 'asdf',
                'name': 'asdf',
                'phone': 'asdf',
                'email': 'asdf',
                'password': 'smth',
                'city_id': 1,
            },
        )
        # assert 1 == 0
        print(response.content)
        # response.status_code
