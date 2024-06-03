from django.contrib import admin

from mailing.models import Client, Message


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email',)
    list_filter = ('last_name',)
    search_fields = ('first_name', 'last_name', 'email',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('theme', 'message',)
    search_fields = ('theme',)
