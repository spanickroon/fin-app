from django import forms
from django.core.exceptions import ValidationError


class AuthUserForm(forms.Form):
    email = forms.EmailField(max_length=254)
    username = forms.CharField(max_length=30)
    password = forms.CharField(
        widget=forms.PasswordInput,
    )

    def clean_password(self) -> str:
        password = self.cleaned_data.get("password")

        if len(password) < 4:
            raise ValidationError("Пароль должен быть не менее 4 символов.")
        return password


class OTPAuthUserForm(AuthUserForm):
    otp = forms.IntegerField()
