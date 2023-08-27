from django.contrib import admin
from main.models import Client, Mails
# Register your models here.

@admin.register(Client)
class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'email',)

@admin.register(Mails)
class MailsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'theme', 'body', 'status', 'logs',)