"""Formulario de autenticación del Sistema Académico."""
from django.contrib.auth.forms import AuthenticationForm
from django import forms


class AccesoForm(AuthenticationForm):
    username = forms.CharField(
        label="Usuario",
        widget=forms.TextInput(attrs={
            "class": "form-control form-control-lg",
            "autocomplete": "username",
            "placeholder": "Ingresa tu usuario",
            "autofocus": True,
        }),
    )
    password = forms.CharField(
        label="Contraseña",
        strip=False,
        widget=forms.PasswordInput(attrs={
            "class": "form-control form-control-lg",
            "autocomplete": "current-password",
            "placeholder": "Ingresa tu contraseña",
        }),
    )
