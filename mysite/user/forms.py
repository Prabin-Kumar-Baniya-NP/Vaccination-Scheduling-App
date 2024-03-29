from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
)
from django.contrib.auth import get_user_model
from django.forms import ModelForm
from django import forms

User = get_user_model()


class SignupForm(UserCreationForm):
    """
    Form to create a new user
    """

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "middle_name",
            "last_name",
            "date_of_birth",
            "gender",
            "photo",
            "identity_document_type",
            "identity_document_number",
        ]


class LoginForm(AuthenticationForm):
    """
    Form to authenticate the user
    """

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = User
        fields = "__all__"


class ChangePasswordForm(PasswordChangeForm):
    """
    Form to change password
    """

    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = User
        fields = "__all__"


class ProfileUpdateForm(ModelForm):
    """
    Form to update the user profile
    """

    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = User
        fields = [
            "first_name",
            "middle_name",
            "last_name",
            "gender",
            "photo",
            "date_of_birth",
            "identity_document_type",
            "identity_document_number",
        ]


class PasswordResetForm(PasswordResetForm):
    """
    Form to reset password
    """

    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class SetPasswordForm(SetPasswordForm):
    """
    Form to set a new password
    """

    def __init__(self, *args, **kwargs):
        super(SetPasswordForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"
