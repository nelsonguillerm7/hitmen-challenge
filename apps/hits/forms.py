# Django core
from django import forms

# Local apps
from apps.hits.models import Hit
from apps.users.models import User


class HitForm(forms.ModelForm):
    """Class defina model the hits"""

    class Meta:
        model = Hit
        fields = (
            "target",
            "description",
            "assigned",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"

        creator = self.initial.get("creator")
        if creator:
            queryset = self.fields["assigned"].queryset
            queryset = queryset.filter(state=User.UserState.ACTIVE)
            if creator.id == 1:
                queryset = queryset.exclude(id__in=[creator.id])
            else:
                queryset = creator.subordinates.filter(
                    state=User.UserState.ACTIVE
                ).exclude(
                    id__in=[1, creator.id],
                )
            self.fields["assigned"].queryset = queryset


class BulkAssignForm(forms.Form):
    hits = forms.ModelMultipleChoiceField(
        queryset=Hit.objects.filter(state=Hit.HitState.ASSIGNED),
        label="Available hits",
    )
    assigned = forms.ModelChoiceField(
        queryset=User.objects.filter(state=User.UserState.ACTIVE).exclude(id=1),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"
