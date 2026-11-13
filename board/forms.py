
from django import forms
from .models import Announcement


class AnnouncementForm(forms.ModelForm):

    class Meta:
        model = Announcement

        fields = [
            'title',
            'description',
            'category',
            'price',
        ]

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Например: Продаю ноутбук'
            }),

            'description': forms.Textarea(attrs={
                'class': 'form-input',
                'placeholder': 'Подробно опишите объявление...',
                'rows': 6
            }),

            'category': forms.Select(attrs={
                'class': 'form-input'
            }),

            'price': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Укажите цену',
                'min': '0',
                'step': '0.01'
            }),
        }
