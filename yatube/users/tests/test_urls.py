from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase

User = get_user_model()


class UsersURLTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(username='test-user')
        cls.url_names = [
            '/auth/signup/',
            '/auth/login/',
            '/auth/password_change/',
            '/auth/password_change/done/',
            '/auth/password_reset/',
            '/auth/password_reset/done/',
            '/auth/reset/<uidb64>/<token>/',
            '/auth/reset/done/',
            '/auth/logout/'
        ]

    def setUp(self) -> None:
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_users_urls_exist_at_desired_location(self):
        """Страницы /signup/ и /login/ доступны анонимному пользователю"""
        for url in self.url_names[:2]:
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_users_urls_authorized_only(self):
        """Страницы /logout/, /password_change/, /password_change/done/,
        /password_reset/, /password_reset/done/, /reset/<uidb64>/<token>/,
        /reset/done/ доступны авторизованному пользователю"""
        for url in self.url_names[2:]:
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)
