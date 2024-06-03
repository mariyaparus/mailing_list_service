from django.db import models

from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    email = models.EmailField(max_length=150, verbose_name='Почта')
    first_name = models.CharField(max_length=50, verbose_name='Имя', **NULLABLE)
    last_name = models.CharField(max_length=50, verbose_name='Фамилия', **NULLABLE)
    comment = models.TextField(verbose_name='Комментарий', **NULLABLE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')

    def __str__(self):
        return f'{self.first_name} {self.last_name}: {self.email}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиент'


class Message(models.Model):
    theme = models.CharField(max_length=150, verbose_name='Тема сообщения', **NULLABLE)
    message = models.TextField(verbose_name='Текст сообщения', **NULLABLE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')

    def __str__(self):
        return f'{self.theme}: {self.message}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
