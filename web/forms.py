from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=20)
    password = forms.CharField(label="Password", widget=forms.PasswordInput())

class SignupForm(forms.Form):
    username = forms.CharField(label="Username", max_length=20)
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Password", widget=forms.PasswordInput())
    passconfirm = forms.CharField(label="Confirm Password", widget=forms.PasswordInput())

class ChainCodeForm(forms.Form):
    code = forms.CharField(label="Code", max_length=6)

class NewChainForm(forms.Form):
    name = forms.CharField(label="Name", max_length=20)
    maxUsers = forms.IntegerField(label="Maximum Users in Chain", max_value=10)
    isPublic = forms.BooleanField(label="Make Chain Public")
