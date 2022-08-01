# Django
from django import forms
from django.contrib.auth.forms import UserCreationForm

# Local apps
from .models import User


class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "first_name", "last_name")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"

    def save(self, commit=True):
        obj = super().save(commit=False)
        obj.username = obj.email
        if commit:
            obj.save()
        return obj


class HitmanBulkAssignedForm(forms.Form):
    hitman = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(
            manager__isnull=True,
            state=User.UserState.ACTIVE,
        ).exclude(id=1),
        label="Available hitman",
    )

    manager = forms.ModelChoiceField(
        queryset=User.objects.filter(
            state=User.UserState.ACTIVE,
        ).exclude(id=1),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"
