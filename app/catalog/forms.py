from django import forms


class CatalogProductsSearchForm(forms.Form):
    search = forms.CharField(
        label='Search',
        max_length=128,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )