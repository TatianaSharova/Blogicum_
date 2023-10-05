from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class PublishedModel(models.Model):
    """Добавляет флаг is_published."""
    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text=('Снимите галочку, чтобы скрыть публикацию.'))

    class Meta:
        abstract = True


class DataTime(models.Model):
    """Поле, в котором указана дата добавления публикации в базу данных."""
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Добавлено')

    class Meta:
        abstract = True


class Category(PublishedModel, DataTime):
    title = models.CharField(max_length=256, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор',
        help_text=('Идентификатор страницы для URL; разрешены '
                   'символы латиницы, цифры, дефис и подчёркивание.')
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title[:30]


class Location(PublishedModel, DataTime):
    name = models.CharField(max_length=256, verbose_name='Название места')

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name[:30]


class Post(PublishedModel, DataTime):
    title = models.CharField(max_length=256, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text=('Если установить дату и время в будущем '
                   '— можно делать отложенные публикации.')
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации',
        related_name='author')
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Местоположение',
        related_name='location')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория',
        related_name='category')
    image = models.ImageField('Фото', upload_to='posts_images', blank=True)

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'

    def __str__(self):
        return self.title[:30]


class Comment(models.Model):
    text = models.TextField('Комментарий')
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post,
                             related_name='comment',
                             on_delete=models.CASCADE)

    class Meta:
        ordering = ('created_at',)
