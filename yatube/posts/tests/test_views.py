import shutil
import tempfile

from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from posts.models import Follow, Group, Post

User = get_user_model()
# Создаем временную папку для медиа-файлов;
# на момент теста медиа папка будет переопределена
TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


# Для сохранения media-файлов в тестах будет использоваться
# временная папка TEMP_MEDIA_ROOT, а потом мы ее удалим
@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostViewTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        cls.uploaded = SimpleUploadedFile(
            name='small.gif',
            content=cls.small_gif,
            content_type='image/gif'
        )
        cls.follower = User.objects.create_user(username='follower')
        cls.author = User.objects.create_user(username='author')
        cls.group = Group.objects.create(title='Бандиты', slug='test-slug')
        cls.post = Post.objects.create(
            text='Рандомные слова',
            author=cls.author,
            group=cls.group,
            image=cls.uploaded
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        # Модуль shutil - библиотека Python с удобными инструментами
        # для управления файлами и директориями:
        # создание, удаление, копирование, перемещение, изменение папок, файлов
        # Метод shutil.rmtree удаляет директорию и всё её содержимое
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.follower_clint = Client()
        self.follower_clint.force_login(self.follower)
        self.authorized_client = Client()
        self.authorized_client.force_login(self.author)

    def test_posts_views_use_correct_templates(self):
        """namespase posts использует соответствующий шаблон."""
        templates_url_names = {
            'posts/index.html': reverse('posts:index'),
            'posts/group_list.html': reverse(
                'posts:group_list', kwargs={'slug': 'test-slug'}),
            'posts/profile.html': reverse(
                'posts:profile', kwargs={'username': 'author'}),
            'posts/post_detail.html': reverse(
                'posts:post_detail', kwargs={'post_id': self.post.id}),
            'posts/create_post.html': reverse('posts:post_create'),
        }
        for template, reverse_name in templates_url_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_post_view_edit_use_correct_template(self):
        """namespase post:edit использует шаблон posts/create_post.html."""
        response = self.authorized_client.get(
            reverse('posts:edit', kwargs={'post_id': self.post.id}))
        self.assertTemplateUsed(response, 'posts/create_post.html')

    def test_index_show_correct_context(self):
        """Шаблон index сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:index'))
        post = response.context['page_obj'][0]
        self.assertEqual(post, self.post)
        self.assertEqual(post.group, self.group)
        self.assertTrue(post.image)

    def test_group_list_show_correct_context(self):
        """Шаблон group_list сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('posts:group_list', kwargs={'slug': 'test-slug'}))
        post = response.context['page_obj'][0]
        self.assertEqual(
            response.context['title'],
            f'Записи сообщества {PostViewTest.group}'
        )
        self.assertEqual(response.context['group'], PostViewTest.group)
        self.assertEqual(post, PostViewTest.post)
        self.assertTrue(post.image)

    def test_profile_show_correct_context(self):
        """Шаблон profile сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('posts:profile', kwargs={'username': 'author'}))
        post = response.context['page_obj'][0]
        self.assertEqual(response.context['author'], PostViewTest.author)
        self.assertEqual(post, PostViewTest.post)
        self.assertEqual(post.group, PostViewTest.group)
        self.assertTrue(post.image)

    def test_post_detail_show_correct_context(self):
        """Шаблон post_detail сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('posts:post_detail', kwargs={'post_id': self.post.id}))
        self.assertEqual(response.context['post'], PostViewTest.post)
        self.assertTrue(response.context['post'].image)

    def test_post_create_show_correct_context(self):
        """Шаблон post_create сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:post_create'))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context['form'].fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_post_edit_show_correct_context(self):
        """Шаблон edit сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('posts:edit', kwargs={'post_id': self.post.id}))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context['form'].fields.get(value)
                self.assertIsInstance(form_field, expected)
        self.assertEqual(response.context['post'], PostViewTest.post)
        self.assertTrue(response.context['is_edit'])

    def test_index_page_cache(self):
        """Проверка работы кеша главной страницы"""
        response = self.client.get(reverse('posts:index'))
        Post.objects.create(text='test', author=self.author)
        response_filled = self.client.get(reverse('posts:index'))
        self.assertEqual(response.content, response_filled.content)

    def test_author_follow_unfollow(self):
        """Тестирование функций подписок на авторов"""
        # Subscribe to the author
        self.follower_clint.get(reverse(
            'posts:profile_follow', args=[self.author])
        )
        # Author creates the post
        post = Post.objects.create(text='Bla-Bla', author=self.author)
        # Get the favorite authors' posts
        response = self.follower_clint.get(reverse('posts:follow_index'))
        # Tests
        self.assertIn(post, response.context['page_obj'])
        self.assertTrue(
            Follow.objects.get(user=self.follower, author=self.author)
        )
        # Unubscribe from the author
        self.follower_clint.get(reverse(
            'posts:profile_unfollow', args=[self.author])
        )
        # Get the favorite authors' posts
        response = self.follower_clint.get(reverse('posts:follow_index'))
        # Tests
        self.assertNotIn(post, response.context['page_obj'])
        self.assertFalse(
            Follow.objects.filter(user=self.follower, author=self.author)
        )
