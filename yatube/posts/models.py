from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name_plural = 'Группы'


class Post(models.Model):
    text = models.TextField(
        help_text='Пиши, не бойся. Тут нет цензуры!',
        verbose_name='Текст поста'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )
    group = models.ForeignKey(
        Group,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='posts',
        help_text='Выбери соответствующую группу или... не выбери',
        verbose_name='Название группы'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор'
    )

    image = models.ImageField(
        'Картинка',
        upload_to='posts/',
        blank=True
    )

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['-pub_date']
        verbose_name_plural = 'Записи'


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        related_name='comments',
        on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        User,
        related_name='comments',
        on_delete=models.CASCADE
    )
    text = models.TextField(
        help_text='Пиши, комментарий!',
        verbose_name='Текст комментария'
    )
    created = models.DateTimeField(
        verbose_name='Дата комментария',
        auto_now_add=True)


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        related_name='follower',
        on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        User,
        related_name='following',
        on_delete=models.CASCADE
    )
