import random
import string

from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from commons.abstract_models import DateTimeBasedModel


class CustomUser(AbstractUser, DateTimeBasedModel):
    phone_number = models.CharField(
        verbose_name=_("Phone Number"),
        max_length=15,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
            )
        ],
        help_text="Enter a valid phone number."
    )
    first_order_placed = models.BooleanField(
        verbose_name=_("First Order Placed"),
        help_text=_("Indicates if the user has placed their first order."),
        default=False
    )
    send_promo_mail = models.BooleanField(
        verbose_name=_("Send Promotional Emails"),
        help_text=_("Indicates if the user agrees to receive promotional emails."),
        default=True
    )

    # Unique referral code
    referral_code = models.CharField(
        verbose_name=_("Referral Code"), max_length=50,
        help_text=_("Unique referral code for the user."), unique=True
    )

    def save(self, *args, **kwargs):
        # Generate unique referral code if not already set
        if not self.referral_code:
            self.referral_code = self.generate_unique_referral_code()
        super().save(*args, **kwargs)

    @staticmethod
    def generate_unique_referral_code():
        """Generates a unique 8-character alphanumeric referral code."""
        while True:
            code = ''.join(
                random.choices(string.ascii_uppercase + string.digits, k=8)
            )
            if not CustomUser.objects.filter(referral_code=code).exists():
                return code

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
