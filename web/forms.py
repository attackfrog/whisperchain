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
