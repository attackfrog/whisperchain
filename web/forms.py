from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

from .models import Chain

class LoginForm(forms.Form):
    username = forms.CharField(label="Username")
    password = forms.CharField(label="Password", widget=forms.PasswordInput())

class SignupForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ["username", "email", "password"]
        widgets = {
            "password": forms.PasswordInput()
        }
    passconfirm = forms.CharField(label="Confirm Password", widget=forms.PasswordInput())

    # the below thanks to https://stackoverflow.com/a/34837887
    def clean(self):
        clean_data = super(SignupForm, self).clean()
        password = clean_data.get("password")
        passconfirm = clean_data.get("passconfirm")
        username = clean_data.get("username")

        validate_password(password, user=username)
        if password != passconfirm:
            raise forms.ValidationError("Those passwords did not match.")

class ChainCodeForm(forms.ModelForm):
    class Meta:
        model = Chain
        fields = ["code"]

class NewChainForm(forms.ModelForm):
    class Meta:
        model = Chain
        fields = ["name", "maxUsers", "isPublic"]
