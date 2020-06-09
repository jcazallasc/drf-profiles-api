import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from profiles.api.serializers import ProfileStatusSerializer
from profiles.models import ProfileStatus


class RegistrationTestCase(APITestCase):

    def test_registration(self):
        data = {
            'username': 'testcase',
            'email': 'test@test.com',
            'password1': 'secret_password',
            'password2': 'secret_password',
        }
        response = self.client.post('/api/rest-auth/registration/', data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ProfileViewSetTestCase(APITestCase):

    list_url = reverse('profile-list')

    def setUp(self):
        self.user = User.objects.create_user(
            username='test_case',
            email='test_case@test.com',
            password='secret_password',
        )
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token {}'.format(self.token.key)
        )

    def test_profile_list_authenticated(self):
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_profile_list_un_authenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_profile_detail_retrieve(self):
        response = self.client.get(
            reverse('profile-detail', kwargs={'pk': self.user.id})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user'], 'test_case')

    def test_profile_update_by_owner(self):
        response = self.client.put(
            reverse('profile-detail', kwargs={'pk': self.user.id}),
            {
                'city': 'Test City',
                'bio': 'Testing',
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user'], 'test_case')
        self.assertEqual(response.data['city'], 'Test City')
        self.assertEqual(response.data['bio'], 'Testing')

    def test_profile_update_by_random_user(self):
        random_user = User.objects.create_user(
            username='random_test',
            password='secret_password',
        )
        self.client.force_authenticate(user=random_user)

        response = self.client.put(
            reverse('profile-detail', kwargs={'pk': self.user.id}),
            {
                'bio': 'hacked!',
            },
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ProfileStatusViewSetTestCase(APITestCase):

    url = reverse('status-list')

    def setUp(self):
        self.user = User.objects.create_user(
            username='test_case',
            email='test_case@test.com',
            password='secret_password',
        )
        self.status = ProfileStatus.objects.create(
            profile=self.user.profile,
            status='status test',
        )
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token {}'.format(self.token.key)
        )

    def test_status_list_authenticated(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_status_list_un_authenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_status_create(self):
        data = {
            'status': 'a new status',
        }
        response = self.client.post(self.url, data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['profile'], 'test_case')
        self.assertEqual(response.data['status'], 'a new status')

    def test_single_status_retrieve(self):
        serializer_data = ProfileStatusSerializer(instance=self.status).data
        response = self.client.get(
            reverse('status-detail', kwargs={'pk': self.status.id}),
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer_data, json.loads(response.content))

    def test_status_update_owner(self):
        response = self.client.put(
            reverse('status-detail', kwargs={'pk': self.status.id}),
            {
                'status': 'updated!'
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'updated!')

    def test_status_update_random_user(self):
        random_user = User.objects.create_user(
            username='random_test',
            password='secret_password',
        )
        self.client.force_authenticate(user=random_user)

        response = self.client.put(
            reverse('status-detail', kwargs={'pk': self.status.id}),
            {
                'status': 'updated!'
            },
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
