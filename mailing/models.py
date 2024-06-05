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


class Mailing(models.Model):
    PERIOD_ONCE = 'Единоразово'
    PERIOD_DAILY = 'Ежедневно'
    PERIOD_WEEKLY = 'Еженедельно'
    PERIOD_MONTHLY = 'Ежемесячно'

    PERIODICITY = (
        (PERIOD_ONCE, 'Единоразово'),
        (PERIOD_DAILY, 'Ежедневно'),
        (PERIOD_WEEKLY, 'Еженедельно'),
        (PERIOD_MONTHLY, 'Ежемесячно'),
    )

    STATUS_CREATED = 'Создана'
    STATUS_STARTED = 'Запущена'
    STATUS_COMPLETED = 'Завершена'

    STATUSES = (
        (STATUS_CREATED, 'Создана'),
        (STATUS_STARTED, 'Запущена'),
        (STATUS_COMPLETED, 'Завершена'),
    )

    time = models.TimeField(verbose_name='Время')
    periodicity = models.CharField(max_length=25, choices=PERIODICITY, default=PERIOD_ONCE,
                                   verbose_name='Периодичность')
    status = models.CharField(max_length=25, choices=STATUSES, default=STATUS_CREATED, verbose_name='Статус')

    client = models.ManyToManyField(Client, verbose_name='Клиент')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='Сообщение', **NULLABLE)

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')

    def __str__(self):
        clients_list = "\n".join([str(client) for client in self.client.all()])
        return (
            f'Время: {self.time}\n'
            f'Клиент:{clients_list}\n'
            f'Сообщение: {self.message}'
        )

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'

        permissions = [
            ('set_status', 'Can change status of mailing')
        ]


class Logs(models.Model):
    STATUS_OK = 'Успешно'
    STATUS_ERROR = 'Ошибка'
    STATUSES = (
        (STATUS_OK, 'Успешно'),
        (STATUS_ERROR, 'Ошибка'),
    )

    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='Рассылка')

    attempt_date = models.DateTimeField(auto_now_add=True, **NULLABLE, verbose_name='Дата и время последней попытки')
    status = models.CharField(choices=STATUSES, default=STATUS_OK, verbose_name='Статус попытки')
    server_response = models.TextField(**NULLABLE, verbose_name='Ответ сервера')

    class Meta:
        verbose_name = 'Лог'
        verbose_name_plural = 'Логи'
