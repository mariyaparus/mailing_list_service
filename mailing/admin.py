from django.contrib import admin

from mailing.models import Client, Message, Mailing, Logs


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email',)
    list_filter = ('last_name',)
    search_fields = ('first_name', 'last_name', 'email',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('theme', 'message',)
    search_fields = ('theme',)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('time', 'periodicity', 'status', 'message',)
    list_filter = ('time',)
    search_fields = ('message',)


@admin.register(Logs)
class LogsAdmin(admin.ModelAdmin):
    list_display = ('mailing', 'attempt_date', 'status', 'server_response',)
    list_filter = ('attempt_date',)
    search_fields = ('mailing',)
