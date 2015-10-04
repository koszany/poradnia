from django import forms
from django.contrib.auth import get_user_model

from atom.forms import FormHorizontalMixin, SaveButtonMixin

from ..models import Profile


class UserForm(FormHorizontalMixin, SaveButtonMixin, forms.ModelForm):
    class Meta:
        # Set this form to use the User model.
        model = get_user_model()

        # Constrain the UserForm to just these fields.
        fields = ("first_name", "last_name")


class ProfileForm(FormHorizontalMixin, SaveButtonMixin, forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("description", "www")
