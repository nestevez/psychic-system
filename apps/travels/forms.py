from django import forms

class NewTrip(forms.Form):
    destination = forms.CharField(label='Destination', max_length=255)
    description = forms.CharField(label='Description', widget=forms.Textarea)
    startdate = forms.DateField(label='Travel Date From', widget=forms.SelectDateWidget)
    enddate = forms.DateField(label='Travel Date To', widget=forms.SelectDateWidget)
