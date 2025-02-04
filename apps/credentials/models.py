import uuid
from django.contrib.auth.models import User
from django.db import models
from django_lifecycle import LifecycleModel


class CategoryAbstract(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100, unique=True)
    icon = models.ImageField(
        upload_to='logos',
        null=True,
        blank=True
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Category(CategoryAbstract):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class UserCategory(CategoryAbstract):
    user = models.ForeignKey(
        'accounts.Account',
        on_delete=models.CASCADE,
        related_name='categories',
    )
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'User Categories'
        verbose_name_plural = 'Users Categories'
        unique_together = ('user', 'name')

    def delete(self, *args, **kwargs):
        self.active = False
        self.save(update_fields=['active'])


class Credential(models.Model):
    user = models.ForeignKey(
        'accounts.Account',
        on_delete=models.CASCADE,
        blank=True,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='+',
        blank=True,
        null=True,
    )
    user_category = models.ForeignKey(
        UserCategory,
        on_delete=models.CASCADE,
        related_name='+',
        blank=True,
        null=True,
    )
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    website = models.URLField()
    notes = models.TextField()

    class Meta:
        verbose_name = 'Credential'
        verbose_name_plural = 'Credentials'

