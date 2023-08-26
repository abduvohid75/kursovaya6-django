from django.contrib import admin
from main.models import User, Mails
# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'email',)

@admin.register(Mails)
class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'theme', 'body', 'status', 'logs',)