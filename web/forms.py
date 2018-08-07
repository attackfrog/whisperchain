from django import forms

from .models import Chain, MAX_CHAIN_NAME_LENGTH, CHAIN_CODE_LENGTH, MAX_USERS_PER_CHAIN

MIN_PASSWORD_LENGTH = 8

class LoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=MAX_CHAIN_NAME_LENGTH)
    password = forms.CharField(label="Password", widget=forms.PasswordInput())

class SignupForm(forms.Form):
    username = forms.CharField(label="Username", max_length=MAX_CHAIN_NAME_LENGTH)
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Password", widget=forms.PasswordInput(), min_length=MIN_PASSWORD_LENGTH)
    passconfirm = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(), min_length=MIN_PASSWORD_LENGTH)

class ChainCodeForm(forms.Form):
    code = forms.CharField(label="Code", max_length=CHAIN_CODE_LENGTH)

class OldChainForm(forms.Form):
    name = forms.CharField(label="Name", max_length=MAX_CHAIN_NAME_LENGTH)
    maxUsers = forms.IntegerField(label="Maximum Users in Chain", max_value=MAX_USERS_PER_CHAIN)
    isPublic = forms.BooleanField(label="Make Chain Public", required=False)

class NewChainForm(forms.ModelForm):
    class Meta:
        model = Chain
        fields = ["name", "maxUsers", "isPublic"]
