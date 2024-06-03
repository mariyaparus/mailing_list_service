from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email','first_name', 'last_name',)
    list_filter = ('email',)
    search_fields = ('first_name', 'last_name',)
