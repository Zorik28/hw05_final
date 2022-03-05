from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

User = get_user_model()


class UserCreateFormTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.guest_client = Client()

    def test_user_create_form(self):
        """Валидная форма создает нового пользователя."""
        users_count = User.objects.count()
        form_date = {
            'username': 'test-user',
            'password1': 'test-password',
            'password2': 'test-password'
        }
        self.guest_client.post(
            reverse('users:signup'),
            data=form_date,
            follow=True
        )
        self.assertEqual(User.objects.count(), users_count + 1)
