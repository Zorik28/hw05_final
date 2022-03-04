from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from posts.models import Group, Post

User = get_user_model()


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create_user(username='author')
        Group.objects.create(title='Бандиты', slug='test-slug')
        cls.post = Post.objects.create(
            text='Рандомные слова',
            author=cls.author
        )

    def setUp(self):
        self.guest_client = Client()
        self.author_client = Client()
        self.author_client.force_login(self.author)
        self.user = User.objects.create_user(username='user')
        self.user_client = Client()
        self.user_client.force_login(self.user)

    def test_post_urls_exist_at_desired_location(self):
        """Страницы: /, /group/<slug>/, /profile/<username>/, /posts/<post_id>/
        доступны любому пользователю."""
        url_names = [
            '/',
            '/group/test-slug/',
            '/profile/author/',
            f'/posts/{self.post.id}/'
        ]
        for address in url_names:
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_urls_redirect_anonymous(self):
        """Редирект страницы /create/, '/posts/<post_id>/edit/',
        'posts/<post_id>/comment/' для анонимного пользователя"""
        url_names = [
            '/create/',
            f'/posts/{self.post.id}/edit/',
            f'/posts/{self.post.id}/comment/'
        ]
        for address in url_names:
            with self.subTest(address=address):
                response = self.guest_client.get(address, follow=True)
                self.assertRedirects(response, f'/auth/login/?next={address}')

    def test_post_url_authorized_only(self):
        """Страница /create/ доступна авторизованному пользователю."""
        response = self.user_client.get('/create/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_url_redirects_not_author(self):
        """Редирект страницы /posts/<post_id>/edit/
        для авторизованного пользователя"""
        response = self.user_client.get(f'/posts/{self.post.id}/edit/')
        self.assertRedirects(response, f'/posts/{self.post.id}/')

    def test_post_url_author_only(self):
        """Cтраница /posts/<post_id>/edit/ доступна автору поста"""
        response = self.author_client.get(f'/posts/{self.post.id}/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = {
            '/': 'posts/index.html',
            '/group/test-slug/': 'posts/group_list.html',
            '/profile/author/': 'posts/profile.html',
            f'/posts/{self.post.id}/': 'posts/post_detail.html',
            f'/posts/{self.post.id}/edit/': 'posts/create_post.html',
            '/create/': 'posts/create_post.html'
        }
        for address, template in templates_url_names.items():
            with self.subTest(address=address):
                response = self.author_client.get(address)
                self.assertTemplateUsed(response, template)

    def test_url_uses_unexisting_page(self):
        """Запрос к несуществующей странице"""
        response = self.author_client.get('/unexisting_page/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
