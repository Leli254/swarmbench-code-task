import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models, transaction
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from .managers import UserManager


class User(AbstractUser):
    """
    Custom user model using email as the primary identifier.
    """

    username = None

    email = models.EmailField(_("email address"), unique=True, db_index=True)
    first_name = models.CharField(
        _("first name"), max_length=100, blank=True, null=True)
    last_name = models.CharField(
        _("last name"), max_length=100, blank=True, null=True)
    phone_number = models.CharField(
        _("phone number"), max_length=20, blank=True)

    uuid_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    is_active = models.BooleanField(default=True)

    date_joined = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: list[str] = []

    objects: "UserManager[User]" = UserManager()  # Add type annotation here

    class Meta:
        ordering = ["-date_joined"]

    def __str__(self) -> str:
        return self.get_full_name() or self.email

    def get_full_name(self) -> str:
        return f"{self.first_name} {self.last_name}".strip() or self.email


class Region(models.Model):
    """
    High-level administrative region (e.g. Nairobi, Nakuru).
    """

    country = models.CharField(_("country"), max_length=100, default="Kenya")
    name = models.CharField(_("region name"), max_length=100, unique=True)
    code = models.SlugField(_("region code"), max_length=50, unique=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("region")
        verbose_name_plural = _("regions")
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class SubRegion(models.Model):
    """
    Sub-division of a Region (e.g. Westlands, CBD, Kilimani).
    """

    region = models.ForeignKey(
        Region,
        on_delete=models.CASCADE,
        related_name="subregions",
        verbose_name=_("region"),
    )

    name = models.CharField(_("sub-region name"), max_length=120)
    code = models.SlugField(_("sub-region code"), max_length=60)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("sub-region")
        verbose_name_plural = _("sub-regions")
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=["region", "name"], name="unique_subregion_per_region"
            )
        ]

    def __str__(self) -> str:
        return f"{self.name} ({self.region.name})"
    
    
class Address(models.Model):
    """
    User delivery address.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="addresses",
    )

    address_name = models.CharField(_("address label"), max_length=100)

    region = models.ForeignKey(
        Region,
        on_delete=models.PROTECT,
        related_name="addresses",
    )
    subregion = models.ForeignKey(
        SubRegion,
        on_delete=models.PROTECT,
        related_name="addresses",
        blank=True,
        null=True,
    )

    phone_number = models.CharField(_("phone number"), max_length=20)
    additional_phone = models.CharField(max_length=20, blank=True)
    delivery_instructions = models.TextField(blank=True, null=True)

    is_default = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-is_default", "-updated_at"]

    def __str__(self) -> str:
        return f"{self.address_name} — {self.user.email}"

    def save(self, *args, **kwargs):
        if self.is_default:
            with transaction.atomic():
                self.__class__.objects.filter(
                    user=self.user, is_default=True
                ).exclude(pk=self.pk).update(is_default=False)
        super().save(*args, **kwargs)


class PickupStation(models.Model):
    """
    Physical pickup station / agent / till point.
    """

    name = models.CharField(_("station name"), max_length=120)

    region = models.ForeignKey(
        Region,
        on_delete=models.PROTECT,
        related_name="pickup_stations",
        blank=True,
        null=True,
    )
    subregion = models.ForeignKey(
        SubRegion,
        on_delete=models.PROTECT,
        related_name="pickup_stations",
        blank=True,
        null=True,
    )

    address = models.CharField(_("physical address"), max_length=255)
    phone_number = models.CharField(_("contact phone"), max_length=20)

    is_active = models.BooleanField(default=True)
    is_default = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-is_default", "name"]
        constraints = [
            models.UniqueConstraint(
                fields=["subregion", "name"],
                name="unique_station_per_subregion",
            )
        ]

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse("users:pickupstation_detail", kwargs={"pk": self.pk})
