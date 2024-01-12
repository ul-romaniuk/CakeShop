from django import forms

from catalog.models import OrderItem, Order


class CatalogProductsSearchForm(forms.Form):
    search = forms.CharField(
        label='Search',
        max_length=128,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )


class AddToCartForm(forms.ModelForm):  # OrderItem
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'order']
        widgets = {
            'product': forms.HiddenInput(),
            'order': forms.HiddenInput(),
        }


class ApplyOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['phone', 'status']
        widgets = {
            'phone': forms.TextInput(),
            'status': forms.HiddenInput()
        }
