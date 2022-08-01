"""Model hits"""
# Django core
from django.db import models
from django_fsm import FSMIntegerField, transition


class Hit(models.Model):
    """Class define model the hits"""

    class HitState(models.IntegerChoices):
        FAILED = 0, "FAILED"
        ASSIGNED = 1, "ASSIGNED"
        COMPLETED = 2, "COMPLETED"

    target = models.CharField(
        max_length=256,
        verbose_name="target",
    )
    assigned = models.ForeignKey(
        "users.User",
        on_delete=models.PROTECT,
        related_name="hits_assigned",
    )
    description = models.TextField(
        verbose_name="description",
    )
    state = FSMIntegerField(
        choices=HitState.choices,
        default=HitState.ASSIGNED,
        protected=True,
    )
    creator = models.ForeignKey(
        "users.User",
        on_delete=models.PROTECT,
        related_name="hits_creators",
    )

    class Meta:
        """Class define information the model"""

        verbose_name = "Hit"
        verbose_name_plural = "Hits"
        ordering = ("-pk",)

    def __str__(self):
        return f"Hit: {self.pk} | Target: {self.target}"

    @transition(
        field="state",
        source=HitState.ASSIGNED,
        target=HitState.COMPLETED,
        custom=dict(
            verbose="Mission complete",
            color="success",
            app="hits",
            model="hit",
        ),
    )
    def completed(self, **kwargs):
        """Method mission complete"""
        pass

    @transition(
        field="state",
        source=HitState.ASSIGNED,
        target=HitState.FAILED,
        custom=dict(
            verbose="Mission failed",
            color="danger",
            app="hits",
            model="hit",
        ),
    )
    def failed(self, **kwargs):
        """Method mission failed"""
        pass
