# Django core
from django.contrib.auth.models import AbstractUser
from django.db import models
from django_fsm import FSMIntegerField, transition


class User(AbstractUser):
    """User model."""

    class UserState(models.IntegerChoices):
        ACTIVE = 1, "ACTIVE"
        INACTIVE = 2, "INACTIVE"

    email = models.EmailField(
        unique=True,
        error_messages={
            "unique": "A user with this email already exists",
        },
    )
    manager = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        null=True,
        related_name="subordinates",
    )
    state = FSMIntegerField(
        choices=UserState.choices,
        default=UserState.ACTIVE,
        protected=True,
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ("pk",)

    def __str__(self):
        """Return username."""
        return f"{self.get_full_name()} ({self.get_state_display()})"

    @transition(
        field="state",
        source=UserState.ACTIVE,
        target=UserState.INACTIVE,
        custom=dict(
            verbose="Inactive hitmen",
            color="danger",
            app="users",
            model="user",
        ),
    )
    def inactive(self, **kwargs):
        self.is_active = False
