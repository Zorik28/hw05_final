from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from posts.models import Group, Post

User = get_user_model()
NUMBER_OF_POSTS = 10


class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='author')
        cls.group = Group.objects.create(title='Бандиты', slug='test-slug')
        for _ in range(13):
            Post.objects.create(
                text='Рандом', author=cls.user, group=cls.group)
        cls.pages = [
            reverse('posts:index'),
            reverse('posts:group_list', kwargs={'slug': 'test-slug'}),
            reverse('posts:profile', kwargs={'username': 'author'})
        ]

    def test_posts_pages_contains_ten_records(self):
        for page in PaginatorViewsTest.pages:
            with self.subTest(page=page):
                response = self.client.get(page)
                self.assertEqual(
                    len(response.context['page_obj']), NUMBER_OF_POSTS
                )

    def test_posts_pages_contains_3_records_on_second_page(self):
        for page in PaginatorViewsTest.pages:
            with self.subTest(page=page):
                response = self.client.get(page, {'page': 2})
                self.assertEqual(len(response.context['page_obj']), 3)
