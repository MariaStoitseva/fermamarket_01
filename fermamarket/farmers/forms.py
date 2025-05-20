from django import forms
from .models import FarmerProfile, Product


class FarmerProfileForm(forms.ModelForm):
    class Meta:
        model = FarmerProfile
        fields = ['farm_name', 'description', 'location', 'phone', 'image']
        widgets = {
            'farm_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Име на фермата'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Кратко описание на вашата ферма',
                'rows': 4
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Локация (напр. Пловдив)'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Телефон за връзка'
            }),

        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'description', 'price', 'quantity', 'weight', 'weight_unit', 'image', 'category']
        labels = {
            'title': 'Име на продукта',
            'description': 'Описание',
            'price': 'Цена',
            'quantity': 'Количество',
            'weight': 'Тегло',
            'weight_unit': 'Мярка',
            'image': 'Снимка',
            'category': 'Категория',
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Име на продукта'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Описание на продукта',
                'rows': 3
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Цена в лева'
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Налично количество'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'weight': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Тегло'
            }),
            'weight_unit': forms.Select(attrs={
                'class': 'form-select'
            }),

        }
