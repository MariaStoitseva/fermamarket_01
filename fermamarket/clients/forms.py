from django import forms
from .models import ClientProfile


class ClientProfileForm(forms.ModelForm):
    class Meta:
        model = ClientProfile
        fields = ['full_name', 'address', 'phone']
        labels = {
            'full_name': 'Име и фамилия',
            'address': 'Адрес за доставка',
            'phone': 'Телефон',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = ClientProfile
        fields = ['full_name', 'address', 'phone']
        labels = {
            'full_name': 'Име и фамилия',
            'address': 'Адрес за доставка',
            'phone': 'Телефон',
        }
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Име и фамилия'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Адрес за доставка'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Телефон'
            }),
        }
