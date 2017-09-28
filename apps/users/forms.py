from django import forms

class RegForm(forms.Form):
    fname = forms.CharField(label="First Name", min_length=2, max_length=50)
    lname = forms.CharField(label="Last Name", min_length=2, max_length=50)
    email = forms.EmailField(label="Email", max_length=255)

class PassForm(forms.Form):
    pw = forms.CharField(label="Password", widget=forms.PasswordInput(), min_length=8)
    cpw = forms.CharField(label="Password Confirmation", widget=forms.PasswordInput())

class LogForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=255)
    pw = forms.CharField(label="Password", widget=forms.PasswordInput(), min_length=8)
