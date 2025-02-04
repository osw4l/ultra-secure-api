import random
from datetime import timezone as dt_tz

import uuid

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.template.loader import render_to_string
from django.utils import timezone
from datetime import timedelta, datetime
from django.db import models, transaction
from django_lifecycle import LifecycleModel, BEFORE_CREATE, hook, AFTER_CREATE
from rest_framework.exceptions import ValidationError

from .managers import UserManager
from apps.utils.email import send_email


class Account(AbstractUser):
    username = None
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    email = models.EmailField(unique=True)

    deleted = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    class Meta:
        verbose_name = "Account"
        verbose_name_plural = "Accounts"

    def __str__(self):
        return self.email

    @transaction.atomic
    def generate_recovery_code(self):
        """
        Generates a 4-digit PIN code and saves it as a Pin instance for the account.
        :return: The generated Pin instance.
        """
        code = f"{random.randint(1000, 9999)}"

        if hasattr(self, 'recovery_pin') and self.recovery_pin:
            now = datetime.now(dt_tz.utc)
            if now < self.recovery_pin.expiration_date:
                # raise ValidationError("A new code cannot be generated. Please wait 10 minutes before requesting a new code.")
                print('generating new code')
            self.recovery_pin.delete()

        return RecoveryPin.objects.create(
            code=code,
            user=self
        )

    def set_new_password(self, password):
        password = make_password(password)
        self.__class__.objects.filter(id=self.id).update(
            password=password
        )
        self.recovery_pin.use_code()


class RecoveryPin(LifecycleModel):
    expiration_date = models.DateTimeField(
        verbose_name="Expiration Date",
        blank=True
    )
    user = models.OneToOneField(
        Account,
        related_name='recovery_pin',
        on_delete=models.CASCADE,
        verbose_name="Account"
    )
    code = models.CharField(max_length=4, verbose_name="Code")

    @hook(BEFORE_CREATE)
    def generate_expiration_date(self):
        """
        Automatically generate the expiration date when the Pin is created.
        Default expiration is 10 minutes from the creation time.
        """
        if not self.expiration_date:
            self.expiration_date = timezone.now() + timedelta(minutes=10)

    @hook(AFTER_CREATE)
    def send_email(self):
        """
        Send an email with the code after the Pin is created using Django's render_to_string.
        """

        context = {
            'first_name': self.user.first_name,
            'code': self.code,
        }

        html_content = render_to_string('code_email.html', context)
        subject = f'Ultra Secure: Reset your password'

        send_email(
            email=self.user.email,
            subject=subject,
            content=html_content
        )

    def is_expired(self):
        """
        Check if the pin has expired.
        """
        return timezone.now() > self.expiration_date

    def use_code(self):
        """
        Use the code. Delete the Pin if it is used or expired.
        """
        if self.is_expired():
            self.delete()
            return False
        self.delete()
        return True