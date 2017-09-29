from django import forms

class RegForm(forms.Form):
    name = forms.CharField(label="Name", min_length=3, max_length=100)
    uname = forms.CharField(label="Username", min_length=3, max_length=255)
    pw = forms.CharField(label="Password", widget=forms.PasswordInput(), min_length=8)
    cpw = forms.CharField(label="Confirm PW", widget=forms.PasswordInput())

class LogForm(forms.Form):
    uname = forms.CharField(label="Username", max_length=255)
    pw = forms.CharField(label="Password", widget=forms.PasswordInput(), min_length=8)
