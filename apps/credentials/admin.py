from django.contrib import admin
from .models import Category, Credential


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'name', 'icon')


@admin.register(Credential)
class CredentialAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'category', 'user_category', 'username', 'password', 'website')