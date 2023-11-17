from django import forms

class LocationForm(forms.Form):
    name = forms.CharField(label='場所名', max_length=100)
    address = forms.CharField(label='住所', max_length=100)
    latitude = forms.CharField(label='緯度', max_length=100)
    longitude = forms.CharField(label='経度', max_length=100)
