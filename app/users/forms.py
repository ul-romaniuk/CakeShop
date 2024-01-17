from django import forms
from django.forms import ModelForm

from users.models import Contact


class CreateMessageForm(ModelForm):
    class Meta:
        model = Contact
        fields = ['email', 'message']
        labels = {
            'email': 'Email',
            'message': 'Повідомлення'
        }
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control',
                                             'placeholder': 'Ваша електронна адреса'}),
            'message': forms.Textarea(attrs={'class': 'form-control',
                                             'placeholder': 'Напишіть ваше повідомлення...'})

        }

