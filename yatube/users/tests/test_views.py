from django import forms
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

User = get_user_model()


class UserViewTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user = User.objects.create_user(username='test-user')

    def setUp(self) -> None:
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_users_views_use_correct_templates(self):
        """namespase users использует соответствующий шаблон."""
        templates_url_names = {
            'users/signup.html': reverse('users:signup'),
            'users/login.html': reverse('users:login'),
            'users/password_change_form.html': reverse(
                'users:password_change'),
            'users/password_change_done.html': reverse(
                'users:password_change_done'),
            'users/password_reset_form.html': reverse(
                'users:password_reset_form'),
            'users/password_reset_done.html': reverse(
                'users:password_reset_done'),
            'users/password_reset_confirm.html': reverse(
                'users:password_reset_confirm',
                args=['Mw', '5si-f7ab5e9f2a875e9b7c61']
            ),
            'users/password_reset_complete.html': reverse(
                'users:password_reset_complete'),
            'users/logged_out.html': reverse('users:logout')
        }
        for template, reverse_name in templates_url_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_signup_show_correct_context(self):
        """Шаблон signup.html сформирован с правильным контекстом."""
        response = self.client.get(reverse('users:signup'))
        form_fields = {
            'first_name': forms.fields.CharField,
            'last_name': forms.fields.CharField,
            'username': forms.fields.CharField,
            'email': forms.fields.EmailField
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context['form'].fields.get(value)
                self.assertIsInstance(form_field, expected)
