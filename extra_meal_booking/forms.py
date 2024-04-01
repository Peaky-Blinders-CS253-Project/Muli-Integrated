from django import forms

class BookExtraMealForm(forms.Form):
    quantity = forms.IntegerField(min_value=1)
