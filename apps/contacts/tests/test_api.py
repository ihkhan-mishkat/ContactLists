from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient

from population_script import add_user, add_contact

from apps.contacts.models import Contact
User = get_user_model()


def create_client(user, url, get=True, kwargs=None):
    token = Token.objects.get_or_create(user=user)[0]
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    if get:
        return client.get(url, kwargs=kwargs)
    return client.pemailt(url, data=kwargs)


class TestUserAPI(APITestCase):
    def setUp(self):
        self.user_data = {'username': 'username', 'password': 'password',
                          'first_name': 'first', 'last_name': 'last',
                          'email': 'email@email.com'}
        self.user = add_user(**self.user_data)

    def test_GET_user(self):
        response = create_client(self.user, reverse('user-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 1)

    def test_GET_user_detail(self):
        response = create_client(
            self.user,
            reverse('user-detail', kwargs={'pk': self.user.pk}))

        updated_dict = {'pk': self.user.pk}
        updated_dict.update(self.user_data)
        del updated_dict['password']

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(dict(response.data), updated_dict)

    def test_POST_user_list(self):
        temp = {'username': 'use', 'password': 'pass', 'email': 'e@email.com'}
        response = create_client(
            self.user,
            reverse('user-list'), get=False, kwargs=temp)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertIn('token', response.data)

    def test_POST_user_detail(self):
        token = Token.objects.get_or_create(user=self.user)[0]
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        name = self.user_data['first_name']
        user = User.objects.filter(first_name=name)[0]
        temp = {'first_name': 'test', 'email': user.email}

        # TODO: Figure out why we need to pass 'email' to make patch request
        response = client.patch(reverse('user-detail', kwargs={'pk': user.pk}),
                                data=temp)

        self.assertNotEqual(user.first_name, response.data['first_name'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(temp['first_name'], response.data['first_name'])


class TestContactAPI(APITestCase):
    def setUp(self):
        self.data = {'username': 'username', 'password': 'password',
                     'first_name': 'first', 'last_name': 'last',
                     'email': 'email@email.com'}
        self.user = add_user(**self.data)
        self.c_data = {'name': 'abc', 'user': self.user,
                       'address': '', 'email': '', 'phone': ''}
        self.contact = add_contact(**self.c_data)

    def test_GET_contact_list(self):
        response = create_client(self.user, reverse('contacts-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Contact.objects.count())

    def test_GET_contact_detail(self):
        response = create_client(
            self.user,
            reverse('contacts-detail', kwargs={'pk': self.contact.pk}))
        temp = {'id': self.contact.pk}
        temp.update(self.c_data)
        temp['user'] = temp['user'].pk

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, temp)

    def test_POST_contact_list(self):
        data = {'name': 'name', 'email': 'email@email.com', 'address': 'address',
                'phone': '+1234567890', 'user': self.c_data['user'].pk}
        response = create_client(self.user, reverse('contacts-list'),
                                 get=False, kwargs=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertDictContainsSubset(data, response.data)

    def test_POST_contact_detail(self):
        data = {'email': 'email@email.com'}
        token = Token.objects.get_or_create(user=self.user)[0]
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.patch(
            reverse('contacts-detail', kwargs={'pk': self.contact.pk}),
            data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], data['email'])
        self.assertNotEqual(self.contact.email, data['email'])
