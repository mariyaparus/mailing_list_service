from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Blog(models.Model):
    title = models.CharField(max_length=150, verbose_name='Заголовок')
    slug = models.CharField(max_length=150, verbose_name='slug', **NULLABLE)
    text = models.TextField(verbose_name='Статья')
    blog_img = models.ImageField(upload_to='blog/', verbose_name='Превью статьи', **NULLABLE)
    created_at = models.DateField(auto_now_add=True, **NULLABLE, verbose_name='Дата создания')
    is_published = models.BooleanField(default=True, verbose_name='Признак публикации')
    views_count = models.IntegerField(default=0, verbose_name='Просмотры')

    def __str__(self):
        return (f'Название: {self.title}'
                f'Дата создания: {self.created_at}'
                f'Опубликовано: {self.is_published}')

    class Meta:
        verbose_name = 'статья'
        verbose_name_plural = 'статьи'
